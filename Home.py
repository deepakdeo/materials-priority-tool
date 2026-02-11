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
from src.theme import render_theme_toggle, apply_theme_css
from src.feedback import render_feedback_widget

# Page configuration
st.set_page_config(
    page_title="Home - Materials Priority Tool",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Check authentication (if enabled)
if not check_password():
    st.stop()

# Render logout button in sidebar
render_logout_button()

# Theme toggle in sidebar
render_theme_toggle()

# Feedback widget in sidebar
render_feedback_widget()

# Apply theme CSS
apply_theme_css()

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

    /* Mobile responsive styles for app components */
    @media (max-width: 768px) {
        .hero-stat {
            padding: 15px;
        }
        .hero-stat h1 {
            font-size: 1.8rem;
        }
        .feature-card {
            padding: 15px;
            margin-bottom: 10px;
            min-height: auto;
        }
        .feature-card h4 {
            font-size: 1rem;
        }
        .feature-card p {
            font-size: 0.85rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("# 🔋 Materials Priority Tool")
st.markdown("##### Data-driven decision support for critical materials prioritization")

# Value proposition - what and why
st.markdown("""
**Which critical materials should the US prioritize for domestic production?**

This tool answers that question using verified government data (USGS, DOE).
Materials are scored on **supply risk**, **strategic importance**, and **production feasibility**,
then ranked to identify priorities. Every number is traceable to source documents.
""")

# Tour button below value proposition
col_tour, col_spacer = st.columns([1, 4])
with col_tour:
    render_tour_button()
st.caption("Take a guided tour to learn how the tool works")

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
        critical_count = len(df[df['short_term_category'] == 'Critical'])
        st.metric(
            label="Critical Materials",
            value=critical_count,
            delta="DOE rated"
        )

    with col3:
        high_import = len(df[df['import_reliance_numeric'] >= 75])
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
            category = row.get('short_term_category', 'Not-Evaluated')
            primary_use = row.get('primary_use', 'N/A')

            # Badge color based on criticality
            if category == "Critical":
                badge = "🔴"
            elif category == "Near-Critical":
                badge = "🟠"
            elif category == "Not-Evaluated":
                badge = "⚪"
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
            height=450,
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
        Materials are scored on **3 factors** (1-10 scale) using only verified data:

        | Factor | Default Weight | What It Measures | Data Source |
        |--------|----------------|------------------|-------------|
        | **Supply Risk** | 40% | Import reliance + producer concentration | USGS MCS 2024 |
        | **Strategic Alignment** | 40% | DOE criticality category | DOE 2023 Assessment |
        | **Production Feasibility** | 20% | Whether US production exists | USGS MCS 2024 |

        The **composite score** is the weighted sum of individual factor scores.
        All data is verified and traceable to government sources.

        Adjust weights in the Trade-off Analysis page to match your priorities.

        ---
        *This framework is extensible. Additional factors (regional logistics advantages, market projections,
        proprietary assessments) can be incorporated as verified data becomes available.*
        """)

    # Materials Grid (collapsed)
    with st.expander("📋 **All Materials** — Complete list with categories", expanded=False):
        display_df = df[['rank', 'material', 'primary_use', 'composite_score',
                         'short_term_category', 'import_reliance_pct']].copy()
        display_df.columns = ['Rank', 'Material', 'Primary Use', 'Score', 'DOE Category', 'Import Reliance']
        display_df = display_df.sort_values('Rank')

        st.dataframe(
            display_df.style.format({
                'Score': '{:.2f}',
            }),
            use_container_width=True,
            hide_index=True,
        )

    # Data sources
    with st.expander("📚 **Data Sources** — Where the data comes from", expanded=False):
        st.markdown("""
        | Source | Description | Link |
        |--------|-------------|------|
        | **USGS Mineral Commodity Summaries 2024** | Import reliance, production, top producers | [usgs.gov/mcs](https://www.usgs.gov/centers/national-minerals-information-center/mineral-commodity-summaries) |
        | **DOE Critical Materials Assessment 2023** | Criticality categories (Critical, Near-Critical, Not-Critical) | [energy.gov/critical-materials](https://www.energy.gov/eere/vehicles/articles/2023-critical-materials-assessment) |
        | **World Bank Pink Sheet** | Historical commodity prices (limited coverage) | [worldbank.org/commodities](https://www.worldbank.org/en/research/commodity-markets) |

        *All data is verified and traceable to source documents. See DATA_SOURCES.md for complete provenance.*
        """)

else:
    st.error("Data not loaded. Please run `python -m src.data_processor` first.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; font-size: 0.9rem;">
    <p><strong>Materials Priority Tool</strong> | Data-driven decision support for critical materials prioritization</p>
    <p>Data sources: USGS MCS 2024 • DOE Critical Materials Assessment 2023</p>
    <p style="margin-top: 10px;">
        Built by <strong>Deepak Deo</strong> |
        <a href="https://github.com/deepakdeo" target="_blank">GitHub</a> •
        <a href="https://linkedin.com/in/deepakdeo" target="_blank">LinkedIn</a>
    </p>
</div>
""", unsafe_allow_html=True)
