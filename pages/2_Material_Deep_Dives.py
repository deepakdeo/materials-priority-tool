"""Material Deep Dives Page - Individual material profiles."""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Material Deep Dives", page_icon="🔍", layout="wide")

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
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.header(selected)
        with col2:
            st.metric("Rank", f"#{int(row['rank'])}")
        with col3:
            category = row["criticality_category"]
            if category == "Critical":
                st.error(f"🔴 {category}")
            elif category == "Near-Critical":
                st.warning(f"🟠 {category}")
            else:
                st.success(f"🟢 {category}")

        st.markdown("---")

        # Score Overview
        st.subheader("Score Overview")

        score_cols = st.columns(6)
        scores = [
            ("Composite", row['composite_score'], None),
            ("Supply Risk", row['supply_risk_score'], "Higher = more risk"),
            ("Market Opp.", row['market_opportunity_score'], "Higher = better opportunity"),
            ("KC Advantage", row['kc_advantage_score'], "Higher = better fit"),
            ("Feasibility", row['production_feasibility_score'], "Higher = more feasible"),
            ("Strategic", row['strategic_alignment_score'], "Higher = better alignment"),
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

            st.metric("Import Reliance", f"{row['import_reliance_pct']}%")
            st.metric("Top Producer", f"{row['top_producer']}")
            st.metric("Top Producer Share", f"{row['top_producer_share_pct']}%")

            production_status = "✅ Yes" if row["us_production_exists"] else "❌ No"
            st.metric("U.S. Production Exists", production_status)

            # Import reliance gauge
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=row['import_reliance_pct'],
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
            # Market Data
            st.subheader("Market Data")

            st.metric("Price (2024)", f"${row['price_2024_usd']:,.0f}/{row['price_unit']}")

            delta_color = "normal" if row["5yr_price_change_pct"] >= 0 else "inverse"
            st.metric("5-Year Price Change", f"{row['5yr_price_change_pct']:+.0f}%")

            st.metric("Demand Growth", f"{row['demand_growth_pct']}%/year")
            st.metric("Market Size", f"${row['market_size_bn']}B")

            # Radar chart for this material
            categories = ['Supply Risk', 'Market Opp.', 'KC Advantage', 'Feasibility', 'Strategic']
            score_values = [
                row['supply_risk_score'],
                row['market_opportunity_score'],
                row['kc_advantage_score'],
                row['production_feasibility_score'],
                row['strategic_alignment_score'],
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

        # Production Feasibility
        st.subheader("Production Feasibility")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Technology Readiness", f"{row['technology_readiness']}/10")

        with col2:
            st.metric("Capital Intensity", f"{row['capex_intensity']}/10",
                      help="Lower is better (easier to deploy)")

        # Data sources
        st.markdown("---")
        st.caption("Data sources: USGS Mineral Commodity Summaries, DOE Critical Materials Assessment")

else:
    st.error("Processed data not found. Please run the data processor first.")
    st.code("python -m src.data_processor", language="bash")
