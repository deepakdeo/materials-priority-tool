"""Data processing script for Materials Priority Tool.

Combines reference data from multiple sources to create unified datasets.
"""

from pathlib import Path

import pandas as pd

from src import PROCESSED_DATA_DIR, REFERENCE_DATA_DIR, RAW_DATA_DIR


def create_materials_master() -> pd.DataFrame:
    """Create the master materials dataset by combining all sources.

    Returns:
        DataFrame with complete material profiles
    """
    # Load reference data
    baseline_df = pd.read_csv(REFERENCE_DATA_DIR / "materials_baseline.csv")
    doe_df = pd.read_csv(REFERENCE_DATA_DIR / "doe_criticality.csv")
    kc_df = pd.read_csv(REFERENCE_DATA_DIR / "kc_logistics.csv")

    # Merge all data
    master = baseline_df.merge(
        doe_df[['material', 'importance_short', 'risk_short', 'importance_medium',
                'risk_medium', 'criticality_category', 'primary_use']],
        on='material',
        how='left'
    )

    master = master.merge(
        kc_df[['material', 'bulk_transport_benefit', 'central_location_benefit',
               'existing_infrastructure', 'kc_notes']],
        on='material',
        how='left'
    )

    return master


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

    # Filter to relevant commodities (nickel is the only one of our 6 materials available)
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


def calculate_scores(master_df: pd.DataFrame) -> pd.DataFrame:
    """Calculate all scoring factors for materials.

    Args:
        master_df: Materials master DataFrame

    Returns:
        DataFrame with calculated scores
    """
    df = master_df.copy()

    # Supply Risk Score (1-10)
    # Higher import reliance and concentration = higher score
    df['supply_risk_score'] = (
        df['import_reliance_pct'] / 100 * 5 +
        df['top_producer_share_pct'] / 100 * 3 +
        2  # base score
    ).clip(1, 10).round(1)

    # Market Opportunity Score (1-10)
    # Higher price growth and demand = higher score
    df['market_opportunity_score'] = (
        df['5yr_price_change_pct'].clip(0, 200) / 50 +
        df['demand_growth_pct'].clip(0, 25) / 5 +
        1  # base score
    ).clip(1, 10).round(1)

    # KC Advantage Score (1-10)
    # Direct from reference data, weighted average
    df['kc_advantage_score'] = (
        df['bulk_transport_benefit'] * 0.4 +
        df['central_location_benefit'] * 0.35 +
        df['existing_infrastructure'] * 0.25
    ).clip(1, 10).round(1)

    # Production Feasibility Score (1-10)
    # Existing production + technology readiness + low capex
    df['production_feasibility_score'] = (
        df['us_production_exists'].astype(int) * 2 +
        df['technology_readiness'] / 2 +
        (11 - df['capex_intensity']) / 3.33
    ).clip(1, 10).round(1)

    # Strategic Alignment Score (1-10)
    # DOE importance and risk scores + battery relevance
    df['strategic_alignment_score'] = (
        (df['importance_short'] + df['risk_short']) / 2 +
        (df['primary_use'] == 'Battery').astype(int) * 2 +
        2  # base score
    ).clip(1, 10).round(1)

    return df


def calculate_composite_scores(
    df: pd.DataFrame,
    weights: dict = None
) -> pd.DataFrame:
    """Calculate composite scores with given weights.

    Args:
        df: DataFrame with individual scores
        weights: Dict of factor weights (must sum to 1.0)

    Returns:
        DataFrame with composite score and rank
    """
    if weights is None:
        weights = {
            'supply_risk_score': 0.25,
            'market_opportunity_score': 0.20,
            'kc_advantage_score': 0.15,
            'production_feasibility_score': 0.20,
            'strategic_alignment_score': 0.20,
        }

    df = df.copy()

    # Calculate composite score
    df['composite_score'] = sum(
        df[col] * weight for col, weight in weights.items()
    ).round(2)

    # Add rank
    df['rank'] = df['composite_score'].rank(ascending=False, method='min').astype(int)

    return df.sort_values('rank')


def save_processed_data():
    """Process and save all data files."""
    # Ensure output directory exists
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Create materials master
    print("Creating materials master dataset...")
    master_df = create_materials_master()

    # Calculate scores
    print("Calculating scores...")
    scored_df = calculate_scores(master_df)
    final_df = calculate_composite_scores(scored_df)

    # Save materials master with scores
    output_path = PROCESSED_DATA_DIR / "materials_master.csv"
    final_df.to_csv(output_path, index=False)
    print(f"Saved: {output_path}")

    # Save scoring inputs (intermediate values)
    scoring_cols = [
        'material', 'import_reliance_pct', 'top_producer_share_pct',
        '5yr_price_change_pct', 'demand_growth_pct', 'us_production_exists',
        'technology_readiness', 'capex_intensity', 'importance_short', 'risk_short',
        'supply_risk_score', 'market_opportunity_score', 'kc_advantage_score',
        'production_feasibility_score', 'strategic_alignment_score',
        'composite_score', 'rank'
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
    print("MATERIALS PRIORITY RANKING")
    print("="*60)
    display_cols = ['rank', 'material', 'composite_score', 'supply_risk_score',
                    'market_opportunity_score', 'kc_advantage_score',
                    'production_feasibility_score', 'strategic_alignment_score',
                    'criticality_category']
    print(df[display_cols].to_string(index=False))
