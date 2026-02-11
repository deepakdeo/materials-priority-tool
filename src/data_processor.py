"""Data processing script for Materials Priority Tool.

Combines verified reference data from multiple sources to create unified datasets.
All data sources are documented in DATA_SOURCES.md

Verified data sources:
- USGS MCS 2024: Import reliance, top producers, US production status
- DOE 2023 Assessment: Criticality categories
- MoDOT/FHWA: KC infrastructure facts
"""

from pathlib import Path

import pandas as pd

from src import PROCESSED_DATA_DIR, REFERENCE_DATA_DIR, RAW_DATA_DIR


def load_verified_baseline() -> pd.DataFrame:
    """Load verified materials baseline from USGS MCS 2024.

    Returns:
        DataFrame with verified supply chain metrics
    """
    filepath = REFERENCE_DATA_DIR / "materials_baseline_verified.csv"
    return pd.read_csv(filepath)


def load_verified_doe_criticality() -> pd.DataFrame:
    """Load verified DOE criticality categories.

    Returns:
        DataFrame with DOE criticality categories
    """
    filepath = REFERENCE_DATA_DIR / "doe_criticality_verified.csv"
    return pd.read_csv(filepath)


def load_kc_infrastructure() -> pd.DataFrame:
    """Load verified KC infrastructure data.

    Returns:
        DataFrame with KC infrastructure metrics
    """
    filepath = REFERENCE_DATA_DIR / "kc_infrastructure.csv"
    return pd.read_csv(filepath)


def create_materials_master() -> pd.DataFrame:
    """Create the master materials dataset by combining verified sources.

    Returns:
        DataFrame with complete material profiles using only verified data
    """
    # Load verified data
    baseline_df = load_verified_baseline()
    doe_df = load_verified_doe_criticality()

    # Merge baseline with DOE criticality
    master = baseline_df.merge(
        doe_df[['material', 'short_term_category', 'medium_term_category', 'primary_use']],
        on='material',
        how='left'
    )

    return master


def convert_import_reliance_to_numeric(value) -> float:
    """Convert import reliance string to numeric value.

    Handles values like '>25', '>50', '>95', '67', etc.
    """
    if isinstance(value, (int, float)):
        return float(value)

    value_str = str(value).strip()
    if value_str.startswith('>'):
        # Use the threshold value (conservative estimate)
        return float(value_str[1:])
    elif value_str.startswith('<'):
        return float(value_str[1:])
    else:
        try:
            return float(value_str)
        except ValueError:
            return 50.0  # Default middle value


def calculate_scores(master_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate scoring factors using only verified data.

    Simplified scoring methodology:
    - Supply Risk: Based on import reliance and producer concentration (verified)
    - DOE Criticality: Based on DOE 2023 categories (verified)
    - US Production: Based on whether domestic production exists (verified)

    REMOVED from scoring (unsourceable):
    - Market opportunity (price, demand growth, market size)
    - KC logistics advantage (subjective scores)
    - Technology readiness
    - Capex intensity

    Args:
        master_df: Materials master DataFrame

    Returns:
        DataFrame with calculated scores
    """
    df = master_df.copy()

    # Convert import reliance to numeric
    df['import_reliance_numeric'] = df['import_reliance_pct'].apply(convert_import_reliance_to_numeric)

    # Supply Risk Score (1-10)
    # Based on verified data: import reliance + producer concentration
    df['supply_risk_score'] = (
        df['import_reliance_numeric'] / 100 * 5 +
        df['top_producer_share_pct'] / 100 * 4 +
        1  # base score
    ).clip(1, 10).round(1)

    # DOE Criticality Score (1-10)
    # Convert categories to numeric scores
    criticality_map = {
        'Critical': 10,
        'Near-Critical': 7,
        'Not-Critical': 4,
        'Not-Evaluated': 5  # Middle value for materials not in DOE assessment
    }
    df['doe_short_term_score'] = df['short_term_category'].map(criticality_map).fillna(5)
    df['doe_medium_term_score'] = df['medium_term_category'].map(criticality_map).fillna(5)

    # Average of short and medium term
    df['strategic_alignment_score'] = (
        (df['doe_short_term_score'] + df['doe_medium_term_score']) / 2
    ).round(1)

    # Production Feasibility Score (1-10)
    # Based only on verified US production status
    df['production_feasibility_score'] = df['us_production_exists'].apply(
        lambda x: 7.0 if x else 4.0
    )

    return df


def calculate_composite_scores(
    df: pd.DataFrame,
    weights: dict = None
) -> pd.DataFrame:
    """Calculate composite scores with given weights.

    Uses simplified 3-factor model based on verified data only:
    - Supply Risk (40%): Higher risk = higher priority for domestic production
    - Strategic Alignment (40%): DOE criticality rating
    - Production Feasibility (20%): US production exists

    Args:
        df: DataFrame with individual scores
        weights: Dict of factor weights (must sum to 1.0)

    Returns:
        DataFrame with composite score and rank
    """
    if weights is None:
        # Simplified weights for verified-only scoring
        weights = {
            'supply_risk_score': 0.40,
            'strategic_alignment_score': 0.40,
            'production_feasibility_score': 0.20,
        }

    df = df.copy()

    # Calculate composite score
    df['composite_score'] = sum(
        df[col] * weight for col, weight in weights.items()
    ).round(2)

    # Add rank
    df['rank'] = df['composite_score'].rank(ascending=False, method='min').astype(int)

    return df.sort_values('rank')


def get_worldbank_prices() -> pd.DataFrame:
    """Load and process World Bank commodity prices.

    Returns:
        DataFrame with monthly prices for available commodities
    """
    wb_file = RAW_DATA_DIR / "worldbank" / "CMO-Historical-Data-Monthly.xlsx"

    if not wb_file.exists():
        return pd.DataFrame()

    df = pd.read_excel(wb_file, sheet_name='Monthly Prices', header=4)

    # Rename first column to date
    df = df.rename(columns={df.columns[0]: 'date'})

    # Convert date column
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Filter to relevant commodities
    commodities = ['date', 'Nickel', 'Aluminum', 'Copper', 'Iron ore, cfr spot']
    available = [c for c in commodities if c in df.columns]

    result = df[available].dropna(subset=['date'])

    return result


def create_price_history() -> pd.DataFrame:
    """Create price history from World Bank data.

    Returns:
        DataFrame with date, material, price columns
    """
    wb_prices = get_worldbank_prices()

    if wb_prices.empty:
        return pd.DataFrame()

    # Melt to long format
    price_cols = [c for c in wb_prices.columns if c != 'date']
    price_history = wb_prices.melt(
        id_vars=['date'],
        value_vars=price_cols,
        var_name='material',
        value_name='price'
    )

    # Filter out null prices
    price_history = price_history.dropna(subset=['price'])

    return price_history


def save_processed_data():
    """Process and save all data files using verified sources only."""
    # Ensure output directory exists
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Create materials master from verified sources
    print("Creating materials master dataset from verified sources...")
    master_df = create_materials_master()

    # Calculate scores using verified data only
    print("Calculating scores (verified data only)...")
    scored_df = calculate_scores(master_df)
    final_df = calculate_composite_scores(scored_df)

    # Save materials master with scores
    output_path = PROCESSED_DATA_DIR / "materials_master.csv"
    final_df.to_csv(output_path, index=False)
    print(f"Saved: {output_path}")

    # Save scoring inputs (intermediate values)
    scoring_cols = [
        'material', 'import_reliance_pct', 'import_reliance_numeric',
        'top_producer', 'top_producer_share_pct', 'us_production_exists',
        'short_term_category', 'medium_term_category', 'primary_use',
        'supply_risk_score', 'strategic_alignment_score',
        'production_feasibility_score', 'composite_score', 'rank'
    ]
    scoring_df = final_df[[c for c in scoring_cols if c in final_df.columns]]
    scoring_path = PROCESSED_DATA_DIR / "scoring_inputs.csv"
    scoring_df.to_csv(scoring_path, index=False)
    print(f"Saved: {scoring_path}")

    # Save World Bank prices
    print("Processing World Bank prices...")
    price_history = create_price_history()
    if not price_history.empty:
        prices_path = PROCESSED_DATA_DIR / "price_history.csv"
        price_history.to_csv(prices_path, index=False)
        print(f"Saved: {prices_path}")

    return final_df


if __name__ == "__main__":
    df = save_processed_data()
    print("\n" + "="*60)
    print("MATERIALS PRIORITY RANKING (Verified Data Only)")
    print("="*60)
    display_cols = ['rank', 'material', 'composite_score', 'supply_risk_score',
                    'strategic_alignment_score', 'production_feasibility_score',
                    'short_term_category']
    available_cols = [c for c in display_cols if c in df.columns]
    print(df[available_cols].to_string(index=False))

    print("\n" + "="*60)
    print("SCORING METHODOLOGY")
    print("="*60)
    print("Supply Risk (40%): Import reliance + producer concentration")
    print("Strategic Alignment (40%): DOE 2023 criticality categories")
    print("Production Feasibility (20%): US domestic production exists")
    print("\nNOTE: Market opportunity and KC advantage removed (unverified data)")
