"""Market Monitor Page - Price trends and market metrics."""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Market Monitor", page_icon="📈", layout="wide")

st.title("📈 Market Monitor")
st.markdown("Price trends, market dynamics, and supply chain metrics.")

# Data paths
DATA_DIR = Path(__file__).parent.parent / "data"
PROCESSED_DIR = DATA_DIR / "processed"


@st.cache_data
def load_materials_data():
    """Load processed materials data."""
    filepath = PROCESSED_DIR / "materials_master.csv"
    if filepath.exists():
        return pd.read_csv(filepath)
    return None


@st.cache_data
def load_price_history():
    """Load price history data."""
    filepath = PROCESSED_DIR / "price_history.csv"
    if filepath.exists():
        df = pd.read_csv(filepath)
        df['date'] = pd.to_datetime(df['date'])
        return df
    return None


# Color scheme
MATERIAL_COLORS = {
    "Lithium": "#1f77b4",
    "Cobalt": "#ff7f0e",
    "Nickel": "#2ca02c",
    "Graphite": "#d62728",
    "Rare Earths": "#9467bd",
    "Manganese": "#8c564b",
    "Copper": "#e377c2",
    "Platinum Group": "#7f7f7f",
    "Gallium": "#bcbd22",
    "Vanadium": "#17becf",
}

df = load_materials_data()
price_df = load_price_history()

if df is not None:
    # Price overview
    st.subheader("Current Prices & Market Size")

    # Price table
    price_cols = ['material', 'price_2024_usd', 'price_unit', '5yr_price_change_pct',
                  'demand_growth_pct', 'market_size_bn']
    price_display = df[price_cols].copy()
    price_display.columns = ['Material', 'Price (USD)', 'Unit', '5Y Change (%)',
                             'Demand Growth (%/yr)', 'Market Size ($B)']

    st.dataframe(
        price_display.style.format({
            'Price (USD)': '${:,.0f}',
            '5Y Change (%)': '{:+.0f}%',
            'Demand Growth (%/yr)': '{:.0f}%',
            'Market Size ($B)': '${:.1f}B',
        }).background_gradient(subset=['5Y Change (%)'], cmap='RdYlGn'),
        width="stretch",
        hide_index=True,
    )

    st.markdown("---")

    # Two column layout
    col1, col2 = st.columns(2)

    with col1:
        # 5-Year Price Changes
        st.subheader("5-Year Price Changes")

        df_sorted = df.sort_values('5yr_price_change_pct', ascending=True)
        colors = ['green' if x >= 0 else 'red' for x in df_sorted['5yr_price_change_pct']]

        fig_price = go.Figure(go.Bar(
            x=df_sorted['5yr_price_change_pct'],
            y=df_sorted['material'],
            orientation='h',
            marker_color=colors,
            text=df_sorted['5yr_price_change_pct'].apply(lambda x: f"{x:+.0f}%"),
            textposition='outside',
        ))

        fig_price.update_layout(
            xaxis_title="Price Change (%)",
            yaxis_title="",
            height=350,
            margin=dict(l=100, r=50, t=20, b=50),
        )

        st.plotly_chart(fig_price, use_container_width=True)

    with col2:
        # Demand Growth Projections
        st.subheader("Demand Growth Projections")

        df_demand = df.sort_values('demand_growth_pct', ascending=True)
        colors = [MATERIAL_COLORS.get(m, "#636EFA") for m in df_demand['material']]

        fig_demand = go.Figure(go.Bar(
            x=df_demand['demand_growth_pct'],
            y=df_demand['material'],
            orientation='h',
            marker_color=colors,
            text=df_demand['demand_growth_pct'].apply(lambda x: f"{x:.0f}%/yr"),
            textposition='outside',
        ))

        fig_demand.update_layout(
            xaxis_title="Annual Demand Growth (%)",
            yaxis_title="",
            height=350,
            margin=dict(l=100, r=50, t=20, b=50),
        )

        st.plotly_chart(fig_demand, use_container_width=True)

    st.markdown("---")

    # Market Size Comparison
    st.subheader("Market Size Comparison")

    df_market = df.sort_values('market_size_bn', ascending=True)
    colors = [MATERIAL_COLORS.get(m, "#636EFA") for m in df_market['material']]

    fig_market = go.Figure(go.Bar(
        x=df_market['market_size_bn'],
        y=df_market['material'],
        orientation='h',
        marker_color=colors,
        text=df_market['market_size_bn'].apply(lambda x: f"${x:.1f}B"),
        textposition='outside',
    ))

    fig_market.update_layout(
        xaxis_title="Market Size ($ Billions)",
        yaxis_title="",
        height=350,
        margin=dict(l=100, r=50, t=20, b=50),
    )

    st.plotly_chart(fig_market, use_container_width=True)

    st.markdown("---")

    # Import Reliance
    st.subheader("Import Reliance & Supply Concentration")

    col1, col2 = st.columns(2)

    with col1:
        # Import Reliance
        df_import = df.sort_values('import_reliance_pct', ascending=True)

        fig_import = go.Figure(go.Bar(
            x=df_import['import_reliance_pct'],
            y=df_import['material'],
            orientation='h',
            marker_color=['red' if x >= 75 else 'orange' if x >= 50 else 'green'
                         for x in df_import['import_reliance_pct']],
            text=df_import['import_reliance_pct'].apply(lambda x: f"{x:.0f}%"),
            textposition='outside',
        ))

        fig_import.update_layout(
            title="Net Import Reliance",
            xaxis_title="Import Reliance (%)",
            yaxis_title="",
            xaxis=dict(range=[0, 110]),
            height=350,
            margin=dict(l=100, r=50, t=40, b=50),
        )

        st.plotly_chart(fig_import, use_container_width=True)

    with col2:
        # Top Producer Concentration
        df_conc = df.sort_values('top_producer_share_pct', ascending=True)

        fig_conc = go.Figure(go.Bar(
            x=df_conc['top_producer_share_pct'],
            y=df_conc['material'],
            orientation='h',
            marker_color=['red' if x >= 70 else 'orange' if x >= 50 else 'green'
                         for x in df_conc['top_producer_share_pct']],
            text=[f"{row['top_producer']} ({row['top_producer_share_pct']:.0f}%)"
                  for _, row in df_conc.iterrows()],
            textposition='outside',
        ))

        fig_conc.update_layout(
            title="Top Producer Concentration",
            xaxis_title="Market Share (%)",
            yaxis_title="",
            xaxis=dict(range=[0, 100]),
            height=350,
            margin=dict(l=100, r=150, t=40, b=50),
        )

        st.plotly_chart(fig_conc, use_container_width=True)

    st.markdown("---")

    # Metrics Correlation Heatmap
    st.subheader("Metrics Correlation Heatmap")
    st.caption("How different metrics relate to each other across materials")

    corr_cols = ['import_reliance_pct', 'top_producer_share_pct', '5yr_price_change_pct',
                 'demand_growth_pct', 'market_size_bn', 'composite_score']
    corr_labels = ['Import Reliance', 'Producer Conc.', '5Y Price Change',
                   'Demand Growth', 'Market Size', 'Composite Score']

    corr_df = df[corr_cols].copy()
    corr_df.columns = corr_labels
    correlation_matrix = corr_df.corr()

    fig_heatmap = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=corr_labels,
        y=corr_labels,
        colorscale='RdBu',
        zmid=0,
        text=correlation_matrix.round(2).values,
        texttemplate='%{text}',
        textfont={"size": 10},
        hoverongaps=False,
    ))

    fig_heatmap.update_layout(
        height=400,
        margin=dict(l=100, r=50, t=20, b=100),
    )

    st.plotly_chart(fig_heatmap, use_container_width=True)

    st.markdown("---")

    # Supply Risk Summary
    st.subheader("Supply Risk Summary")

    risk_data = []
    for _, row in df.iterrows():
        risk_level = "🔴 High" if row['import_reliance_pct'] >= 75 else \
                     "🟠 Medium" if row['import_reliance_pct'] >= 50 else "🟢 Low"
        risk_data.append({
            'Material': row['material'],
            'Import Reliance': f"{row['import_reliance_pct']}%",
            'Top Producer': row['top_producer'],
            'Concentration': f"{row['top_producer_share_pct']}%",
            'U.S. Production': '✅' if row['us_production_exists'] else '❌',
            'Risk Level': risk_level,
        })

    st.dataframe(pd.DataFrame(risk_data), width="stretch", hide_index=True)

    # World Bank price history (if available)
    if price_df is not None and not price_df.empty:
        st.markdown("---")
        st.subheader("Historical Commodity Prices (World Bank)")
        st.caption("Note: Only Nickel is available from World Bank Pink Sheet among our target materials")

        # Filter to last 10 years
        recent_prices = price_df[price_df['date'] >= '2015-01-01']

        if 'Nickel' in recent_prices['material'].values:
            nickel_prices = recent_prices[recent_prices['material'] == 'Nickel']

            fig_history = px.line(
                nickel_prices,
                x='date',
                y='price',
                title='Nickel Price History ($/metric ton)',
            )

            fig_history.update_layout(
                xaxis_title="Date",
                yaxis_title="Price ($/mt)",
                height=400,
            )

            st.plotly_chart(fig_history, use_container_width=True)

    st.markdown("---")
    st.caption("Data sources: USGS Mineral Commodity Summaries 2024, World Bank Pink Sheet, Industry Reports")
    st.caption("Note: Prices and market data are point-in-time estimates. For real-time data, consult LME or industry sources.")

else:
    st.error("Processed data not found. Please run the data processor first.")
    st.code("python -m src.data_processor", language="bash")
