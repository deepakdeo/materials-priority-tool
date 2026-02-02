"""Material Deep Dives Page - Individual material profiles."""

import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Material Deep Dives", page_icon="🔍", layout="wide")

st.title("🔍 Material Deep Dives")
st.markdown("Detailed profiles for each critical material.")

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

    # Material selector
    materials = df["material"].tolist()
    selected = st.selectbox("Select a material to explore:", materials)

    if selected:
        row = df[df["material"] == selected].iloc[0]

        # Header with criticality badge
        col1, col2 = st.columns([3, 1])
        with col1:
            st.header(selected)
        with col2:
            category = row["criticality_category"]
            if category == "Critical":
                st.error(f"🔴 {category}")
            elif category == "Near-Critical":
                st.warning(f"🟠 {category}")
            else:
                st.success(f"🟢 {category}")

        st.markdown("---")

        # Key metrics
        st.subheader("Key Statistics")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Import Reliance", f"{row['import_reliance_pct']}%")

        with col2:
            st.metric("Top Producer", row["top_producer"])

        with col3:
            st.metric("Top Producer Share", f"{row['top_producer_share_pct']}%")

        with col4:
            production_status = "✅ Yes" if row["us_production_exists"] else "❌ No"
            st.metric("U.S. Production", production_status)

        st.markdown("---")

        # Market data
        st.subheader("Market Data")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Price (2024)", f"${row['price_2024_usd']:,}/{row['price_unit']}")

        with col2:
            delta_color = "normal" if row["5yr_price_change_pct"] >= 0 else "inverse"
            st.metric("5-Year Price Change", f"{row['5yr_price_change_pct']}%")

        with col3:
            st.metric("Demand Growth", f"{row['demand_growth_pct']}%/year")

        with col4:
            st.metric("Market Size", f"${row['market_size_bn']}B")

        st.markdown("---")

        # DOE Assessment
        st.subheader("DOE Critical Materials Assessment")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Short-term (2023-2027)**")
            st.write(f"- Importance to Energy: {row['importance_short']}/4")
            st.write(f"- Supply Risk: {row['risk_short']}/4")

        with col2:
            st.markdown("**Medium-term (2028-2035)**")
            st.write(f"- Importance to Energy: {row['importance_medium']}/4")
            st.write(f"- Supply Risk: {row['risk_medium']}/4")

        st.markdown("---")

        # KC Advantage
        st.subheader("Kansas City Advantage Assessment")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Bulk Transport Benefit", f"{row['bulk_transport_benefit']}/10")

        with col2:
            st.metric("Central Location Benefit", f"{row['central_location_benefit']}/10")

        with col3:
            st.metric("Existing Infrastructure", f"{row['existing_infrastructure']}/10")

        st.info(f"**Notes:** {row['kc_notes']}")

        st.markdown("---")

        # Production feasibility
        st.subheader("Production Feasibility")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Technology Readiness", f"{row['technology_readiness']}/10")

        with col2:
            st.metric("Capital Intensity", f"{row['capex_intensity']}/10")

        st.markdown("---")
        st.info("📌 Price history charts and supply chain diagrams will be added in Phase 4.")

except FileNotFoundError as e:
    st.error(f"Data file not found: {e}")
except Exception as e:
    st.error(f"Error loading data: {e}")
