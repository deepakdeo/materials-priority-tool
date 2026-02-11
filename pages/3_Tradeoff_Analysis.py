"""Trade-off Analysis Page - Interactive weight adjustment."""

import json
import sys
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.tour import render_tour_widget
from src.auth import check_password, render_logout_button
from src.theme import render_theme_toggle, apply_theme_css
from src.feedback import render_feedback_widget

st.set_page_config(page_title="Trade-off Analysis", page_icon="⚖️", layout="wide")

# Check authentication
if not check_password():
    st.stop()

render_logout_button()
render_theme_toggle()
render_feedback_widget()
apply_theme_css()

# Render tour widget if active
render_tour_widget()

st.title("⚖️ Trade-off Analysis")
st.markdown("Adjust scoring weights to explore different prioritization scenarios.")

# Initialize session state for saved scenarios
if "saved_scenarios" not in st.session_state:
    st.session_state.saved_scenarios = {}

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
    # Sidebar with weight sliders
    st.sidebar.header("Adjust Weights")
    st.sidebar.markdown("Weights must sum to 100%")

    # Preset scenarios
    st.sidebar.markdown("---")
    st.sidebar.subheader("Preset Scenarios")

    preset = st.sidebar.selectbox(
        "Load preset:",
        ["Custom", "Default (Balanced)", "Supply Security Focus", "Strategic Focus", "Feasibility Focus"]
    )

    # Set default values based on preset or loaded scenario (3-factor model)
    if "load_weights" in st.session_state:
        lw = st.session_state.pop("load_weights")
        default_weights = (
            lw["supply_risk"], lw["strategic_alignment"], lw["production_feasibility"]
        )
    elif preset == "Default (Balanced)":
        default_weights = (40, 40, 20)
    elif preset == "Supply Security Focus":
        default_weights = (60, 25, 15)
    elif preset == "Strategic Focus":
        default_weights = (25, 60, 15)
    elif preset == "Feasibility Focus":
        default_weights = (30, 30, 40)
    else:
        default_weights = (40, 40, 20)

    st.sidebar.markdown("---")

    w_supply = st.sidebar.slider("Supply Risk", 0, 80, default_weights[0], 5,
                                  help="Import reliance + producer concentration")
    w_strategic = st.sidebar.slider("Strategic Alignment", 0, 80, default_weights[1], 5,
                                     help="DOE criticality categories")
    w_feasibility = st.sidebar.slider("Production Feasibility", 0, 80, default_weights[2], 5,
                                       help="US production exists")

    total_weight = w_supply + w_strategic + w_feasibility

    if total_weight != 100:
        st.sidebar.error(f"⚠️ Weights sum to {total_weight}%. Must equal 100%.")
        weights_valid = False
    else:
        st.sidebar.success("✓ Weights sum to 100%")
        weights_valid = True

    # Scenario Save/Load Section
    st.sidebar.markdown("---")
    st.sidebar.subheader("Save/Load Scenarios")

    # Save current scenario
    scenario_name = st.sidebar.text_input("Scenario name:", placeholder="My Custom Scenario")
    if st.sidebar.button("💾 Save Current Scenario") and scenario_name:
        st.session_state.saved_scenarios[scenario_name] = {
            "supply_risk": w_supply,
            "strategic_alignment": w_strategic,
            "production_feasibility": w_feasibility,
            "saved_at": datetime.now().isoformat(),
        }
        st.sidebar.success(f"Saved: {scenario_name}")

    # Load saved scenario
    if st.session_state.saved_scenarios:
        saved_names = list(st.session_state.saved_scenarios.keys())
        selected_scenario = st.sidebar.selectbox("Load saved scenario:", [""] + saved_names)
        if selected_scenario and st.sidebar.button("📂 Load Scenario"):
            scenario = st.session_state.saved_scenarios[selected_scenario]
            st.session_state["load_weights"] = scenario
            st.rerun()

    # Export scenarios as JSON
    if st.session_state.saved_scenarios:
        scenarios_json = json.dumps(st.session_state.saved_scenarios, indent=2)
        st.sidebar.download_button(
            label="📥 Export All Scenarios",
            data=scenarios_json,
            file_name="weight_scenarios.json",
            mime="application/json",
        )

    # Import scenarios from JSON
    uploaded_file = st.sidebar.file_uploader("📤 Import Scenarios", type="json", key="scenario_upload")
    if uploaded_file is not None:
        try:
            imported = json.load(uploaded_file)
            st.session_state.saved_scenarios.update(imported)
            st.sidebar.success(f"Imported {len(imported)} scenario(s)")
        except json.JSONDecodeError:
            st.sidebar.error("Invalid JSON file")

    # Show current weights
    st.subheader("Current Weight Configuration")

    col1, col2, col3 = st.columns(3)
    col1.metric("Supply Risk", f"{w_supply}%")
    col2.metric("Strategic Alignment", f"{w_strategic}%")
    col3.metric("Feasibility", f"{w_feasibility}%")

    st.markdown("---")

    if weights_valid:
        # Recalculate composite scores with new weights (3-factor model)
        df_calc = df.copy()
        df_calc['new_composite'] = (
            df_calc['supply_risk_score'] * (w_supply / 100) +
            df_calc['strategic_alignment_score'] * (w_strategic / 100) +
            df_calc['production_feasibility_score'] * (w_feasibility / 100)
        ).round(2)

        df_calc['new_rank'] = df_calc['new_composite'].rank(ascending=False, method='min').astype(int)
        df_calc = df_calc.sort_values('new_rank')

        # Show rank changes
        df_calc['rank_change'] = df_calc['rank'] - df_calc['new_rank']

        # Two column layout
        col_left, col_right = st.columns([1.5, 1])

        with col_left:
            # Rankings with current weights
            st.subheader("Rankings with Current Weights")

            display_cols = [
                "new_rank", "material", "new_composite",
                "supply_risk_score", "strategic_alignment_score",
                "production_feasibility_score", "rank_change"
            ]

            def format_rank_change(val):
                if val > 0:
                    return f"↑{val}"
                elif val < 0:
                    return f"↓{abs(val)}"
                return "—"

            display_df = df_calc[display_cols].copy()
            display_df['rank_change'] = display_df['rank_change'].apply(format_rank_change)

            st.dataframe(
                display_df.style.format({
                    "new_composite": "{:.2f}",
                    "supply_risk_score": "{:.1f}",
                    "strategic_alignment_score": "{:.1f}",
                    "production_feasibility_score": "{:.1f}",
                }),
                width="stretch",
                hide_index=True,
                column_config={
                    "new_rank": "Rank",
                    "material": "Material",
                    "new_composite": "Score",
                    "supply_risk_score": "Supply",
                    "strategic_alignment_score": "Strategic",
                    "production_feasibility_score": "Feasibility",
                    "rank_change": "Change",
                }
            )

        with col_right:
            # Bar chart comparison
            st.subheader("Score Comparison")

            df_sorted = df_calc.sort_values('new_composite', ascending=True)
            colors = [MATERIAL_COLORS.get(m, "#636EFA") for m in df_sorted['material']]

            fig = go.Figure(go.Bar(
                x=df_sorted['new_composite'],
                y=df_sorted['material'],
                orientation='h',
                marker_color=colors,
                text=df_sorted['new_composite'].round(2),
                textposition='outside',
            ))

            fig.update_layout(
                xaxis_title="Composite Score",
                yaxis_title="",
                xaxis=dict(range=[0, 10]),
                height=350,
                margin=dict(l=100, r=50, t=20, b=50),
            )

            st.plotly_chart(fig, use_container_width=True)

        # Top pick highlight
        top_material = df_calc.iloc[0]["material"]
        top_score = df_calc.iloc[0]["new_composite"]
        original_rank = int(df_calc.iloc[0]["rank"])

        st.markdown("---")

        if original_rank == 1:
            st.success(f"**Top Priority:** {top_material} (Score: {top_score:.2f}) — Remains #1")
        else:
            st.info(f"**Top Priority:** {top_material} (Score: {top_score:.2f}) — Was #{original_rank} with default weights")

        # Sensitivity insight
        st.markdown("---")
        st.subheader("Sensitivity Insights")

        # Find which weight change would change the #1 rank
        current_top = df_calc.iloc[0]['material']
        runner_up = df_calc.iloc[1]['material']
        score_gap = df_calc.iloc[0]['new_composite'] - df_calc.iloc[1]['new_composite']

        st.write(f"**Current leader:** {current_top} leads {runner_up} by {score_gap:.2f} points")

        # Calculate which factor gives runner_up the biggest advantage
        runner_up_row = df_calc[df_calc['material'] == runner_up].iloc[0]
        top_row = df_calc[df_calc['material'] == current_top].iloc[0]

        factors = ['supply_risk_score', 'strategic_alignment_score', 'production_feasibility_score']
        factor_names = ['Supply Risk', 'Strategic Alignment', 'Production Feasibility']

        advantages = []
        for factor, name in zip(factors, factor_names):
            diff = runner_up_row[factor] - top_row[factor]
            if diff > 0:
                advantages.append((name, diff))

        if advantages:
            advantages.sort(key=lambda x: x[1], reverse=True)
            st.write(f"**{runner_up}** could overtake **{current_top}** by increasing weight on:")
            for name, diff in advantages[:2]:
                st.write(f"  • {name} (advantage: +{diff:.1f})")

    else:
        st.warning("⚠️ Please adjust weights in the sidebar to sum to 100%.")

    st.markdown("---")
    st.caption("Adjust the sliders in the sidebar to see how different weight configurations affect the rankings.")

else:
    st.error("Processed data not found. Please run the data processor first.")
    st.code("python -m src.data_processor", language="bash")
