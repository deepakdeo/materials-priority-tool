"""Supply Chain Monitor Page - Import reliance and supply concentration metrics."""

import sys
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.tour import render_tour_widget
from src.auth import check_password, render_logout_button
from src.theme import render_theme_toggle, apply_theme_css
from src.feedback import render_feedback_widget

st.set_page_config(page_title="Supply Chain Monitor", page_icon="📈", layout="wide")

# Check authentication
if not check_password():
    st.stop()

render_logout_button()
render_theme_toggle()
render_feedback_widget()
apply_theme_css()

# Render tour widget if active
render_tour_widget()

st.title("📈 Supply Chain Monitor")
st.markdown("Import reliance, supply concentration, and DOE criticality metrics from verified sources.")

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
    "Tin": "#aec7e8",
    "Tungsten": "#ffbb78",
    "Zinc": "#98df8a",
}

df = load_materials_data()
price_df = load_price_history()

if df is not None:
    # Supply Chain Overview Table
    st.subheader("Supply Chain Overview")

    supply_cols = ['material', 'import_reliance_pct', 'top_producer', 'top_producer_share_pct',
                   'us_production_exists', 'short_term_category']
    supply_display = df[supply_cols].copy()
    supply_display['us_production_exists'] = supply_display['us_production_exists'].apply(
        lambda x: '✅' if x else '❌'
    )
    supply_display.columns = ['Material', 'Import Reliance', 'Top Producer', 'Producer Share (%)',
                              'US Production', 'DOE Category']

    st.dataframe(
        supply_display,
        width="stretch",
        hide_index=True,
    )

    st.markdown("---")

    # Import Reliance & Supply Concentration
    st.subheader("Import Reliance & Supply Concentration")

    col1, col2 = st.columns(2)

    with col1:
        # Import Reliance
        df_import = df.copy()
        df_import = df_import.sort_values('import_reliance_numeric', ascending=True)

        fig_import = go.Figure(go.Bar(
            x=df_import['import_reliance_numeric'],
            y=df_import['material'],
            orientation='h',
            marker_color=['red' if x >= 75 else 'orange' if x >= 50 else 'green'
                         for x in df_import['import_reliance_numeric']],
            text=df_import['import_reliance_pct'].apply(lambda x: f"{x}"),
            textposition='outside',
        ))

        fig_import.update_layout(
            title="Net Import Reliance (USGS MCS 2024)",
            xaxis_title="Import Reliance (%)",
            yaxis_title="",
            xaxis=dict(range=[0, 110]),
            height=400,
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
            title="Top Producer Concentration (USGS MCS 2024)",
            xaxis_title="Market Share (%)",
            yaxis_title="",
            xaxis=dict(range=[0, 100]),
            height=400,
            margin=dict(l=100, r=150, t=40, b=50),
        )

        st.plotly_chart(fig_conc, use_container_width=True)

    st.markdown("---")

    # DOE Criticality Matrix
    st.subheader("DOE Criticality Categories (2023)")
    st.caption("Source: DOE Critical Materials Assessment 2023")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Short-Term (2020-2025)**")
        short_term_counts = df['short_term_category'].value_counts()
        fig_short = px.pie(
            values=short_term_counts.values,
            names=short_term_counts.index,
            color=short_term_counts.index,
            color_discrete_map={
                'Critical': '#d62728',
                'Near-Critical': '#ff7f0e',
                'Not-Critical': '#2ca02c',
                'Not-Evaluated': '#7f7f7f',
            }
        )
        fig_short.update_layout(height=300)
        st.plotly_chart(fig_short, use_container_width=True)

    with col2:
        st.markdown("**Medium-Term (2025-2035)**")
        med_term_counts = df['medium_term_category'].value_counts()
        fig_med = px.pie(
            values=med_term_counts.values,
            names=med_term_counts.index,
            color=med_term_counts.index,
            color_discrete_map={
                'Critical': '#d62728',
                'Near-Critical': '#ff7f0e',
                'Not-Critical': '#2ca02c',
                'Not-Evaluated': '#7f7f7f',
            }
        )
        fig_med.update_layout(height=300)
        st.plotly_chart(fig_med, use_container_width=True)

    st.markdown("---")

    # Supply Risk Summary
    st.subheader("Supply Risk Summary")

    risk_data = []
    for _, row in df.iterrows():
        import_val = row.get('import_reliance_numeric', 50)
        risk_level = "🔴 High" if import_val >= 75 else \
                     "🟠 Medium" if import_val >= 50 else "🟢 Low"
        risk_data.append({
            'Material': row['material'],
            'Import Reliance': str(row['import_reliance_pct']),
            'Top Producer': row['top_producer'],
            'Concentration': f"{row['top_producer_share_pct']}%",
            'U.S. Production': '✅' if row['us_production_exists'] else '❌',
            'DOE Short-Term': row.get('short_term_category', 'N/A'),
            'DOE Medium-Term': row.get('medium_term_category', 'N/A'),
            'Risk Level': risk_level,
        })

    st.dataframe(pd.DataFrame(risk_data), width="stretch", hide_index=True)

    st.markdown("---")

    # Correlation between supply risk factors
    st.subheader("Supply Risk Factor Correlation")
    st.caption("How supply chain metrics relate to each other")

    corr_cols = ['import_reliance_numeric', 'top_producer_share_pct', 'supply_risk_score',
                 'strategic_alignment_score', 'composite_score']
    corr_labels = ['Import Reliance', 'Producer Conc.', 'Supply Risk Score',
                   'Strategic Score', 'Composite Score']

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

    # World Bank price history (if available)
    if price_df is not None and not price_df.empty:
        st.markdown("---")
        st.subheader("Historical Commodity Prices (World Bank)")
        st.caption("Note: World Bank Pink Sheet covers limited commodities (Nickel, Copper, Aluminum)")

        # Filter to last 10 years
        recent_prices = price_df[price_df['date'] >= '2015-01-01']

        available_materials = recent_prices['material'].unique().tolist()
        if available_materials:
            selected_material = st.selectbox("Select commodity:", available_materials)
            mat_prices = recent_prices[recent_prices['material'] == selected_material]

            fig_history = px.line(
                mat_prices,
                x='date',
                y='price',
                title=f'{selected_material} Price History',
            )

            fig_history.update_layout(
                xaxis_title="Date",
                yaxis_title="Price",
                height=400,
            )

            st.plotly_chart(fig_history, use_container_width=True)

    st.markdown("---")
    st.caption("Data sources: USGS Mineral Commodity Summaries 2024, DOE Critical Materials Assessment 2023")
    st.caption("World Bank Commodity Markets Outlook (for historical prices where available)")

else:
    st.error("Processed data not found. Please run the data processor first.")
    st.code("python -m src.data_processor", language="bash")
