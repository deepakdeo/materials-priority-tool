"""Material Deep Dives Page - Individual material profiles."""

import sys
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.tour import render_tour_widget
from src.auth import check_password, render_logout_button
from src.theme import render_theme_toggle, apply_theme_css
from src.feedback import render_feedback_widget

st.set_page_config(page_title="Material Deep Dives", page_icon="🔍", layout="wide")

# Check authentication
if not check_password():
    st.stop()

render_logout_button()
render_theme_toggle()
render_feedback_widget()
apply_theme_css()

# Render tour widget if active
render_tour_widget()

st.title("🔍 Material Deep Dives")
st.markdown("Detailed profiles for each critical material.")

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

if df is not None:
    # Material selector
    materials = df.sort_values('rank')['material'].tolist()
    selected = st.selectbox("Select a material to explore:", materials)

    if selected:
        row = df[df["material"] == selected].iloc[0]
        color = MATERIAL_COLORS.get(selected, "#636EFA")

        # Header with rank and criticality badge
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        with col1:
            st.header(selected)
        with col2:
            st.metric("Rank", f"#{int(row['rank'])}")
        with col3:
            st.metric("Primary Use", row.get("primary_use", "N/A"))
        with col4:
            category = row.get("short_term_category", "Not-Evaluated")
            if category == "Critical":
                st.error(f"🔴 {category}")
            elif category == "Near-Critical":
                st.warning(f"🟠 {category}")
            elif category == "Not-Evaluated":
                st.info(f"⚪ {category}")
            else:
                st.success(f"🟢 {category}")

        st.markdown("---")

        # Score Overview
        st.subheader("Score Overview")

        score_cols = st.columns(4)
        scores = [
            ("Composite", row['composite_score'], "Weighted average of all factors"),
            ("Supply Risk", row['supply_risk_score'], "Import reliance + producer concentration (40%)"),
            ("Strategic", row['strategic_alignment_score'], "DOE criticality category (40%)"),
            ("Feasibility", row['production_feasibility_score'], "US production exists (20%)"),
        ]

        for i, (name, score, help_text) in enumerate(scores):
            with score_cols[i]:
                st.metric(name, f"{score:.1f}/10", help=help_text)

        st.markdown("---")

        # Two column layout
        left_col, right_col = st.columns(2)

        with left_col:
            # Supply Chain Overview
            st.subheader("Supply Chain Overview")

            # Handle import reliance as string (e.g., ">25")
            import_reliance_display = str(row['import_reliance_pct'])
            if not import_reliance_display.startswith('>') and not import_reliance_display.startswith('<'):
                import_reliance_display = f"{import_reliance_display}%"

            st.metric("Import Reliance", import_reliance_display)
            st.metric("Top Producer", f"{row['top_producer']}")
            st.metric("Top Producer Share", f"{row['top_producer_share_pct']}%")

            production_status = "✅ Yes" if row["us_production_exists"] else "❌ No"
            st.metric("U.S. Production Exists", production_status)

            # Import reliance gauge - use numeric value
            import_numeric = row.get('import_reliance_numeric', 50)
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=import_numeric,
                domain={'x': [0, 1], 'y': [0, 1]},
                title={'text': "Import Reliance %"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': color},
                    'steps': [
                        {'range': [0, 25], 'color': "lightgreen"},
                        {'range': [25, 50], 'color': "yellow"},
                        {'range': [50, 75], 'color': "orange"},
                        {'range': [75, 100], 'color': "lightcoral"},
                    ],
                }
            ))
            fig_gauge.update_layout(height=250, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_gauge, use_container_width=True)

        with right_col:
            # Score Breakdown
            st.subheader("Score Profile")

            # Radar chart for this material - 3-factor model
            categories = ['Supply Risk', 'Strategic Alignment', 'Production Feasibility']
            score_values = [
                row['supply_risk_score'],
                row['strategic_alignment_score'],
                row['production_feasibility_score'],
            ]
            score_values.append(score_values[0])

            fig_radar = go.Figure(go.Scatterpolar(
                r=score_values,
                theta=categories + [categories[0]],
                fill='toself',
                line_color=color,
                fillcolor=color,
                opacity=0.6,
            ))
            fig_radar.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
                showlegend=False,
                height=300,
                margin=dict(l=40, r=40, t=20, b=20),
            )
            st.plotly_chart(fig_radar, use_container_width=True)

            # Score breakdown table
            st.markdown("**Score Breakdown:**")
            st.write(f"- Supply Risk: {row['supply_risk_score']:.1f}/10 (40% weight)")
            st.write(f"- Strategic Alignment: {row['strategic_alignment_score']:.1f}/10 (40% weight)")
            st.write(f"- Production Feasibility: {row['production_feasibility_score']:.1f}/10 (20% weight)")

        st.markdown("---")

        # DOE Assessment
        st.subheader("DOE Critical Materials Assessment (2023)")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Short-term (2020-2025)**")
            short_cat = row.get('short_term_category', 'Not-Evaluated')
            if short_cat == "Critical":
                st.error(f"🔴 {short_cat}")
            elif short_cat == "Near-Critical":
                st.warning(f"🟠 {short_cat}")
            elif short_cat == "Not-Evaluated":
                st.info(f"⚪ {short_cat}")
            else:
                st.success(f"🟢 {short_cat}")

        with col2:
            st.markdown("**Medium-term (2025-2035)**")
            med_cat = row.get('medium_term_category', 'Not-Evaluated')
            if med_cat == "Critical":
                st.error(f"🔴 {med_cat}")
            elif med_cat == "Near-Critical":
                st.warning(f"🟠 {med_cat}")
            elif med_cat == "Not-Evaluated":
                st.info(f"⚪ {med_cat}")
            else:
                st.success(f"🟢 {med_cat}")

        primary_use = row.get('primary_use', 'N/A')
        st.caption(f"Primary Use: {primary_use}")

        # Data sources
        st.markdown("---")
        st.caption("Data sources: USGS Mineral Commodity Summaries 2024, DOE Critical Materials Assessment 2023")

else:
    st.error("Processed data not found. Please run the data processor first.")
    st.code("python -m src.data_processor", language="bash")
