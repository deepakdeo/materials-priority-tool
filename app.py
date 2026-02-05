"""Materials Priority Tool - Main Entry Point.

A Streamlit dashboard for scoring and ranking critical materials
to support supply chain prioritization decisions.
"""

import sys
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))
from src.tour import render_tour_widget, render_tour_button
from src.auth import check_password, render_logout_button

# Page configuration
st.set_page_config(
    page_title="Materials Priority Tool",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Check authentication (if enabled)
if not check_password():
    st.stop()

# Render logout button in sidebar
render_logout_button()

# Render tour widget at top if active
render_tour_widget()

# Data paths
DATA_DIR = Path(__file__).parent / "data"
PROCESSED_DIR = DATA_DIR / "processed"


@st.cache_data
def load_materials_data():
    """Load processed materials data."""
    filepath = PROCESSED_DIR / "materials_master.csv"
    if filepath.exists():
        return pd.read_csv(filepath)
    return None


# Load data
df = load_materials_data()

# Custom CSS for styling
st.markdown("""
<style>
    .hero-stat {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .hero-stat h1 {
        margin: 0;
        font-size: 2.5rem;
    }
    .hero-stat p {
        margin: 5px 0 0 0;
        opacity: 0.9;
    }
    .feature-card {
        background: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        height: 100%;
    }
    .material-badge-critical {
        background: #ff4444;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
    }
    .material-badge-near {
        background: #ffaa00;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
    }
    .material-badge-lower {
        background: #44aa44;
        color: white;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("# 🔋 Materials Priority Tool")
st.markdown("##### Data-driven decision support for critical materials prioritization")

# Tour button in hero area
col_tour, col_spacer = st.columns([1, 4])
with col_tour:
    render_tour_button()

st.markdown("---")

if df is not None:
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Materials Analyzed",
            value=len(df),
            delta="Comprehensive coverage"
        )

    with col2:
        critical_count = len(df[df['criticality_category'] == 'Critical'])
        st.metric(
            label="Critical Materials",
            value=critical_count,
            delta="DOE rated"
        )

    with col3:
        high_import = len(df[df['import_reliance_pct'] >= 75])
        st.metric(
            label="High Import Risk",
            value=f"{high_import}",
            delta=f"≥75% import reliant"
        )

    with col4:
        top_material = df.sort_values('rank').iloc[0]['material']
        st.metric(
            label="Top Priority",
            value=top_material,
            delta="Highest composite score"
        )

    st.markdown("---")

    # Two column layout: Top Rankings + Mini Chart
    col_left, col_right = st.columns([1.2, 1])

    with col_left:
        st.markdown("### 🏆 Top Priority Materials")

        # Top 5 materials display
        top_5 = df.sort_values('rank').head(5)

        for _, row in top_5.iterrows():
            rank = int(row['rank'])
            material = row['material']
            score = row['composite_score']
            category = row['criticality_category']
            primary_use = row.get('primary_use', 'N/A')

            # Badge color based on criticality
            if category == "Critical":
                badge = "🔴"
            elif category == "Near-Critical":
                badge = "🟠"
            else:
                badge = "🟢"

            col_rank, col_info, col_score = st.columns([0.5, 3, 1])

            with col_rank:
                st.markdown(f"### #{rank}")

            with col_info:
                st.markdown(f"**{material}**")
                st.caption(f"{primary_use} • {badge} {category}")

            with col_score:
                st.markdown(f"### {score:.2f}")
                st.caption("score")

    with col_right:
        st.markdown("### 📊 Score Overview")

        # Mini bar chart
        chart_df = df.sort_values('composite_score', ascending=True)

        colors = ['#667eea' if i >= len(chart_df) - 3 else '#d0d0d0'
                  for i in range(len(chart_df))]

        fig = go.Figure(go.Bar(
            x=chart_df['composite_score'],
            y=chart_df['material'],
            orientation='h',
            marker_color=colors,
            text=chart_df['composite_score'].round(2),
            textposition='outside',
        ))

        fig.update_layout(
            xaxis_title="Composite Score",
            yaxis_title="",
            xaxis=dict(range=[0, 10]),
            height=350,
            margin=dict(l=10, r=50, t=10, b=30),
            showlegend=False,
        )

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Feature Cards
    st.markdown("### 🚀 Quick Actions")

    feat_col1, feat_col2, feat_col3, feat_col4 = st.columns(4)

    with feat_col1:
        st.markdown("""
        <div class="feature-card">
            <h4>📊 Priority Rankings</h4>
            <p>View complete rankings with export options (CSV, Excel, PDF)</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Rankings →", key="btn_rankings"):
            st.switch_page("pages/1_Priority_Rankings.py")

    with feat_col2:
        st.markdown("""
        <div class="feature-card">
            <h4>🔍 Deep Dives</h4>
            <p>Explore individual material profiles and supply chain details</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Explore Materials →", key="btn_dives"):
            st.switch_page("pages/2_Material_Deep_Dives.py")

    with feat_col3:
        st.markdown("""
        <div class="feature-card">
            <h4>⚖️ Trade-off Analysis</h4>
            <p>Adjust weights and save custom prioritization scenarios</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Analyze Trade-offs →", key="btn_tradeoff"):
            st.switch_page("pages/3_Tradeoff_Analysis.py")

    with feat_col4:
        st.markdown("""
        <div class="feature-card">
            <h4>🎲 Uncertainty Analysis</h4>
            <p>Monte Carlo simulation for ranking confidence intervals</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Run Simulation →", key="btn_monte"):
            st.switch_page("pages/5_Uncertainty_Analysis.py")

    st.markdown("---")

    # Scoring Framework (collapsed by default)
    with st.expander("📐 **Scoring Framework** — How materials are evaluated", expanded=False):
        st.markdown("""
        Materials are scored on **5 factors** (1-10 scale) with configurable weights:

        | Factor | Default Weight | What It Measures |
        |--------|----------------|------------------|
        | **Supply Risk** | 25% | U.S. import dependency, geographic concentration |
        | **Market Opportunity** | 20% | Price trends, demand growth projections |
        | **KC Advantage** | 15% | Kansas City logistics benefits (rail, river, central location) |
        | **Production Feasibility** | 20% | Domestic production technology readiness |
        | **Strategic Alignment** | 20% | DOE criticality rating, battery/EV/defense relevance |

        The **composite score** is the weighted sum of individual factor scores.
        Adjust weights in the Trade-off Analysis page to match your priorities.
        """)

    # Materials Grid (collapsed)
    with st.expander("📋 **All Materials** — Complete list with categories", expanded=False):
        display_df = df[['rank', 'material', 'primary_use', 'composite_score',
                         'criticality_category', 'import_reliance_pct']].copy()
        display_df.columns = ['Rank', 'Material', 'Primary Use', 'Score', 'DOE Category', 'Import %']
        display_df = display_df.sort_values('Rank')

        st.dataframe(
            display_df.style.format({
                'Score': '{:.2f}',
                'Import %': '{:.0f}%'
            }),
            use_container_width=True,
            hide_index=True,
        )

    # Data sources
    with st.expander("📚 **Data Sources** — Where the data comes from", expanded=False):
        st.markdown("""
        - **USGS Mineral Commodity Summaries 2024** — Production, imports, prices
        - **DOE Critical Materials Assessment 2023** — Criticality ratings
        - **World Bank Pink Sheet** — Historical commodity prices
        - **Bureau of Transportation Statistics** — KC logistics metrics
        """)

else:
    st.error("Data not loaded. Please run `python -m src.data_processor` first.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.9rem;">
    <p>Materials Priority Tool | Data-driven decision support for critical materials prioritization</p>
    <p>Data sources: USGS • DOE • World Bank</p>
</div>
""", unsafe_allow_html=True)
