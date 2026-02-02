"""Data loading functions for Materials Priority Tool.

This module handles loading and parsing data from:
- USGS Mineral Commodity Summaries
- USGS Historical Statistics (DS-140)
- World Bank Pink Sheet
- DOE Critical Materials Assessment
- Reference data (KC logistics, DOE criticality scores)
"""

from pathlib import Path
from typing import Optional

import pandas as pd

from src import (
    MATERIALS_LIST,
    PROCESSED_DATA_DIR,
    RAW_DATA_DIR,
    REFERENCE_DATA_DIR,
)


def load_doe_criticality() -> pd.DataFrame:
    """Load DOE criticality scores from reference data.

    Returns:
        DataFrame with columns: material, importance_short, risk_short,
        importance_medium, risk_medium, criticality_category
    """
    filepath = REFERENCE_DATA_DIR / "doe_criticality.csv"
    if not filepath.exists():
        raise FileNotFoundError(f"DOE criticality data not found at {filepath}")
    return pd.read_csv(filepath)


def load_kc_logistics() -> pd.DataFrame:
    """Load KC (Kansas City) logistics advantage reference data.

    Returns:
        DataFrame with KC logistics metrics per material
    """
    filepath = REFERENCE_DATA_DIR / "kc_logistics.csv"
    if not filepath.exists():
        raise FileNotFoundError(f"KC logistics data not found at {filepath}")
    return pd.read_csv(filepath)


def load_materials_master() -> pd.DataFrame:
    """Load the unified materials master dataset.

    Returns:
        DataFrame with all materials and their attributes/scores
    """
    filepath = PROCESSED_DATA_DIR / "materials_master.csv"
    if not filepath.exists():
        raise FileNotFoundError(f"Materials master data not found at {filepath}")
    return pd.read_csv(filepath)


def load_price_history() -> pd.DataFrame:
    """Load historical price data for all materials.

    Returns:
        DataFrame with columns: date, material, price, unit
    """
    filepath = PROCESSED_DATA_DIR / "price_history.csv"
    if not filepath.exists():
        raise FileNotFoundError(f"Price history data not found at {filepath}")
    df = pd.read_csv(filepath)
    df["date"] = pd.to_datetime(df["date"])
    return df


def load_scoring_inputs() -> pd.DataFrame:
    """Load pre-computed scoring inputs.

    Returns:
        DataFrame with all intermediate values used for scoring
    """
    filepath = PROCESSED_DATA_DIR / "scoring_inputs.csv"
    if not filepath.exists():
        raise FileNotFoundError(f"Scoring inputs data not found at {filepath}")
    return pd.read_csv(filepath)


def load_usgs_commodity(material: str) -> Optional[pd.DataFrame]:
    """Load USGS commodity data for a specific material.

    Args:
        material: Name of the material (e.g., 'Lithium', 'Cobalt')

    Returns:
        DataFrame with USGS data or None if not found
    """
    # USGS files are typically named in lowercase
    material_lower = material.lower().replace(" ", "_")

    # Try CSV first, then Excel
    csv_path = RAW_DATA_DIR / "usgs" / f"{material_lower}.csv"
    if csv_path.exists():
        return pd.read_csv(csv_path)

    xlsx_path = RAW_DATA_DIR / "usgs" / f"{material_lower}.xlsx"
    if xlsx_path.exists():
        return pd.read_excel(xlsx_path)

    return None


def load_worldbank_prices() -> Optional[pd.DataFrame]:
    """Load World Bank Pink Sheet commodity prices.

    Returns:
        DataFrame with monthly commodity prices or None if not found
    """
    # Look for the Pink Sheet file
    for filename in ["CMO-Historical-Data-Monthly.xlsx", "pinksheet.xlsx", "worldbank_prices.xlsx"]:
        filepath = RAW_DATA_DIR / "worldbank" / filename
        if filepath.exists():
            return pd.read_excel(filepath)

    return None


def get_available_materials() -> list[str]:
    """Get list of materials with available data.

    Returns:
        List of material names that have data loaded
    """
    available = []
    for material in MATERIALS_LIST:
        if load_usgs_commodity(material) is not None:
            available.append(material)
    return available if available else MATERIALS_LIST
