"""Market Monitor Page - Price trends and volatility analysis."""

import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Market Monitor", page_icon="📈", layout="wide")

st.title("📈 Market Monitor")
st.markdown("Price trends, volatility metrics, and market dynamics.")

# Load reference data
DATA_DIR = Path(__file__).parent.parent / "data" / "reference"


@st.cache_data
def load_baseline_data():
    """Load baseline materials data."""
    return pd.read_csv(DATA_DIR / "materials_baseline.csv")


try:
    df = load_baseline_data()

    # Price overview
    st.subheader("Current Prices (2024)")

    # Display price table
    price_df = df[["material", "price_2024_usd", "price_unit", "5yr_price_change_pct", "market_size_bn"]].copy()
    price_df.columns = ["Material", "Price (USD)", "Unit", "5-Year Change (%)", "Market Size ($B)"]

    st.dataframe(
        price_df.style.format({
            "Price (USD)": "{:,.0f}",
            "5-Year Change (%)": "{:+.0f}%",
            "Market Size ($B)": "${:.1f}B",
        }),
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("---")

    # Price change visualization (placeholder)
    st.subheader("5-Year Price Changes")

    # Create a simple visualization of price changes
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Gainers**")
        gainers = df[df["5yr_price_change_pct"] > 0].sort_values("5yr_price_change_pct", ascending=False)
        for _, row in gainers.iterrows():
            st.write(f"📈 **{row['material']}**: +{row['5yr_price_change_pct']}%")

    with col2:
        st.markdown("**Decliners**")
        decliners = df[df["5yr_price_change_pct"] <= 0].sort_values("5yr_price_change_pct")
        for _, row in decliners.iterrows():
            st.write(f"📉 **{row['material']}**: {row['5yr_price_change_pct']}%")

    st.markdown("---")

    # Demand growth
    st.subheader("Demand Growth Projections")

    growth_df = df[["material", "demand_growth_pct"]].sort_values("demand_growth_pct", ascending=False)

    for _, row in growth_df.iterrows():
        st.progress(row["demand_growth_pct"] / 25, text=f"{row['material']}: {row['demand_growth_pct']}%/year")

    st.markdown("---")

    # Import reliance
    st.subheader("Import Reliance")

    import_df = df[["material", "import_reliance_pct", "top_producer", "top_producer_share_pct"]].copy()
    import_df = import_df.sort_values("import_reliance_pct", ascending=False)

    for _, row in import_df.iterrows():
        color = "🔴" if row["import_reliance_pct"] >= 75 else "🟠" if row["import_reliance_pct"] >= 50 else "🟢"
        st.write(f"{color} **{row['material']}**: {row['import_reliance_pct']}% import reliant (Top: {row['top_producer']} @ {row['top_producer_share_pct']}%)")

    st.markdown("---")
    st.info("📌 Interactive price trend charts with range selectors will be added in Phase 5.")

except FileNotFoundError as e:
    st.error(f"Data file not found: {e}")
except Exception as e:
    st.error(f"Error loading data: {e}")
