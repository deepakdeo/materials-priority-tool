"""Materials Priority Tool - Core modules."""

from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).parent.parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
REFERENCE_DATA_DIR = DATA_DIR / "reference"

# Target materials for analysis
MATERIALS_LIST = [
    "Lithium",
    "Cobalt",
    "Nickel",
    "Graphite",
    "Rare Earths",
    "Manganese",
    "Copper",
    "Platinum Group",
    "Gallium",
    "Vanadium",
]

# Default scoring weights (must sum to 1.0)
DEFAULT_WEIGHTS = {
    "supply_risk": 0.25,
    "market_opportunity": 0.20,
    "kc_advantage": 0.15,
    "production_feasibility": 0.20,
    "strategic_alignment": 0.20,
}
