"""Priority Rankings Page - Composite scores and material rankings."""

import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Priority Rankings", page_icon="📊", layout="wide")

st.title("📊 Priority Rankings")
st.markdown("Composite scores and rankings for all critical materials.")

# Load reference data
DATA_DIR = Path(__file__).parent.parent / "data" / "reference"


@st.cache_data
def load_baseline_data():
    """Load baseline materials data."""
    filepath = DATA_DIR / "materials_baseline.csv"
    if filepath.exists():
        return pd.read_csv(filepath)
    return None


@st.cache_data
def load_doe_data():
    """Load DOE criticality data."""
    filepath = DATA_DIR / "doe_criticality.csv"
    if filepath.exists():
        return pd.read_csv(filepath)
    return None


@st.cache_data
def load_kc_data():
    """Load KC logistics data."""
    filepath = DATA_DIR / "kc_logistics.csv"
    if filepath.exists():
        return pd.read_csv(filepath)
    return None


# Load data
baseline_df = load_baseline_data()
doe_df = load_doe_data()
kc_df = load_kc_data()

if baseline_df is not None and doe_df is not None and kc_df is not None:
    # Merge data
    merged = baseline_df.merge(doe_df, on="material").merge(
        kc_df[["material", "bulk_transport_benefit", "central_location_benefit", "existing_infrastructure"]],
        on="material"
    )

    # Calculate scores (simplified for Phase 1)
    merged["supply_risk_score"] = (
        merged["import_reliance_pct"] / 100 * 5 +
        merged["top_producer_share_pct"] / 100 * 3 +
        2  # base score
    ).clip(1, 10)

    merged["market_opportunity_score"] = (
        merged["5yr_price_change_pct"].clip(0, 100) / 25 +
        merged["demand_growth_pct"].clip(0, 20) / 5 +
        2  # base score
    ).clip(1, 10)

    merged["kc_advantage_score"] = (
        merged["bulk_transport_benefit"] * 0.4 +
        merged["central_location_benefit"] * 0.35 +
        merged["existing_infrastructure"] * 0.25
    ).clip(1, 10)

    merged["production_feasibility_score"] = (
        merged["us_production_exists"].astype(int) * 2 +
        merged["technology_readiness"] / 2 +
        (11 - merged["capex_intensity"]) / 3.33
    ).clip(1, 10)

    merged["strategic_alignment_score"] = (
        (merged["importance_short"] + merged["risk_short"]) / 2 +
        3  # battery relevance base
    ).clip(1, 10)

    # Calculate composite score with default weights
    weights = {
        "supply_risk_score": 0.25,
        "market_opportunity_score": 0.20,
        "kc_advantage_score": 0.15,
        "production_feasibility_score": 0.20,
        "strategic_alignment_score": 0.20,
    }

    merged["composite_score"] = sum(
        merged[col] * weight for col, weight in weights.items()
    ).round(2)

    merged["rank"] = merged["composite_score"].rank(ascending=False, method="min").astype(int)
    merged = merged.sort_values("rank")

    # Display rankings table
    st.subheader("Material Rankings")

    display_cols = [
        "rank", "material", "composite_score",
        "supply_risk_score", "market_opportunity_score", "kc_advantage_score",
        "production_feasibility_score", "strategic_alignment_score",
        "criticality_category"
    ]

    st.dataframe(
        merged[display_cols].style.format({
            "composite_score": "{:.2f}",
            "supply_risk_score": "{:.1f}",
            "market_opportunity_score": "{:.1f}",
            "kc_advantage_score": "{:.1f}",
            "production_feasibility_score": "{:.1f}",
            "strategic_alignment_score": "{:.1f}",
        }),
        use_container_width=True,
        hide_index=True,
    )

    # Summary cards
    st.subheader("Top 3 Priority Materials")

    cols = st.columns(3)
    for i, (_, row) in enumerate(merged.head(3).iterrows()):
        with cols[i]:
            st.metric(
                label=f"#{row['rank']} {row['material']}",
                value=f"{row['composite_score']:.2f}",
                delta=row["criticality_category"],
            )
            st.caption(f"Top producer: {row['top_producer']} ({row['top_producer_share_pct']}%)")

    st.markdown("---")
    st.info("📌 Full visualizations (bar chart, radar chart) will be added in Phase 3.")

else:
    st.error("Reference data files not found. Please ensure data files are in place.")
    st.markdown("""
    Expected files:
    - `data/reference/materials_baseline.csv`
    - `data/reference/doe_criticality.csv`
    - `data/reference/kc_logistics.csv`
    """)
