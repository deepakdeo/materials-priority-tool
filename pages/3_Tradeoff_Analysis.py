"""Trade-off Analysis Page - Interactive weight adjustment."""

import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Trade-off Analysis", page_icon="⚖️", layout="wide")

st.title("⚖️ Trade-off Analysis")
st.markdown("Adjust scoring weights to explore different prioritization scenarios.")

# Load reference data
DATA_DIR = Path(__file__).parent.parent / "data" / "reference"


@st.cache_data
def load_all_data():
    """Load and merge all reference data."""
    baseline = pd.read_csv(DATA_DIR / "materials_baseline.csv")
    doe = pd.read_csv(DATA_DIR / "doe_criticality.csv")
    kc = pd.read_csv(DATA_DIR / "kc_logistics.csv")
    return baseline.merge(doe, on="material").merge(kc, on="material")


try:
    df = load_all_data()

    # Sidebar with weight sliders
    st.sidebar.header("Adjust Weights")
    st.sidebar.markdown("Weights must sum to 100%")

    w_supply = st.sidebar.slider("Supply Risk", 0, 50, 25, 5, help="Import dependency & concentration")
    w_market = st.sidebar.slider("Market Opportunity", 0, 50, 20, 5, help="Price trends & demand growth")
    w_kc = st.sidebar.slider("KC Advantage", 0, 50, 15, 5, help="Kansas City logistics benefits")
    w_feasibility = st.sidebar.slider("Production Feasibility", 0, 50, 20, 5, help="Domestic production readiness")
    w_strategic = st.sidebar.slider("Strategic Alignment", 0, 50, 20, 5, help="DOE & national priorities")

    total_weight = w_supply + w_market + w_kc + w_feasibility + w_strategic

    if total_weight != 100:
        st.sidebar.error(f"Weights sum to {total_weight}%. Must equal 100%.")
        weights_valid = False
    else:
        st.sidebar.success("✓ Weights sum to 100%")
        weights_valid = True

    # Calculate scores
    df["supply_risk_score"] = (
        df["import_reliance_pct"] / 100 * 5 +
        df["top_producer_share_pct"] / 100 * 3 +
        2
    ).clip(1, 10)

    df["market_opportunity_score"] = (
        df["5yr_price_change_pct"].clip(0, 100) / 25 +
        df["demand_growth_pct"].clip(0, 20) / 5 +
        2
    ).clip(1, 10)

    df["kc_advantage_score"] = (
        df["bulk_transport_benefit"] * 0.4 +
        df["central_location_benefit"] * 0.35 +
        df["existing_infrastructure"] * 0.25
    ).clip(1, 10)

    df["production_feasibility_score"] = (
        df["us_production_exists"].astype(int) * 2 +
        df["technology_readiness"] / 2 +
        (11 - df["capex_intensity"]) / 3.33
    ).clip(1, 10)

    df["strategic_alignment_score"] = (
        (df["importance_short"] + df["risk_short"]) / 2 +
        3
    ).clip(1, 10)

    # Calculate composite with user weights
    if weights_valid:
        df["composite_score"] = (
            df["supply_risk_score"] * (w_supply / 100) +
            df["market_opportunity_score"] * (w_market / 100) +
            df["kc_advantage_score"] * (w_kc / 100) +
            df["production_feasibility_score"] * (w_feasibility / 100) +
            df["strategic_alignment_score"] * (w_strategic / 100)
        ).round(2)

        df["rank"] = df["composite_score"].rank(ascending=False, method="min").astype(int)
        df = df.sort_values("rank")

        # Show current weights
        st.subheader("Current Weight Configuration")

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Supply Risk", f"{w_supply}%")
        col2.metric("Market Opp.", f"{w_market}%")
        col3.metric("KC Advantage", f"{w_kc}%")
        col4.metric("Feasibility", f"{w_feasibility}%")
        col5.metric("Strategic", f"{w_strategic}%")

        st.markdown("---")

        # Rankings with current weights
        st.subheader("Rankings with Current Weights")

        display_cols = [
            "rank", "material", "composite_score",
            "supply_risk_score", "market_opportunity_score", "kc_advantage_score",
            "production_feasibility_score", "strategic_alignment_score"
        ]

        st.dataframe(
            df[display_cols].style.format({
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

        # Top pick highlight
        top_material = df.iloc[0]["material"]
        top_score = df.iloc[0]["composite_score"]

        st.success(f"**Top Priority:** {top_material} (Score: {top_score:.2f})")

        st.markdown("---")

        # Preset scenarios
        st.subheader("Preset Scenarios")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("**Supply Security Focus**")
            st.caption("Supply Risk: 40%, Strategic: 30%, others: 10% each")

        with col2:
            st.markdown("**Market Opportunity Focus**")
            st.caption("Market: 35%, Feasibility: 30%, others lower")

        with col3:
            st.markdown("**KC Advantage Focus**")
            st.caption("KC Advantage: 35%, Feasibility: 25%, others: 13-14%")

        st.info("📌 Click preset buttons to auto-apply scenarios (coming in Phase 4).")

    else:
        st.warning("Please adjust weights in the sidebar to sum to 100%.")

except FileNotFoundError as e:
    st.error(f"Data file not found: {e}")
except Exception as e:
    st.error(f"Error loading data: {e}")
