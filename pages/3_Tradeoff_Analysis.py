"""Trade-off Analysis Page - Interactive weight adjustment."""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Trade-off Analysis", page_icon="⚖️", layout="wide")

st.title("⚖️ Trade-off Analysis")
st.markdown("Adjust scoring weights to explore different prioritization scenarios.")

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
    # Sidebar with weight sliders
    st.sidebar.header("Adjust Weights")
    st.sidebar.markdown("Weights must sum to 100%")

    # Preset scenarios
    st.sidebar.markdown("---")
    st.sidebar.subheader("Preset Scenarios")

    preset = st.sidebar.selectbox(
        "Load preset:",
        ["Custom", "Default (Balanced)", "Supply Security Focus", "Market Opportunity Focus", "KC Advantage Focus"]
    )

    # Set default values based on preset
    if preset == "Default (Balanced)":
        default_weights = (25, 20, 15, 20, 20)
    elif preset == "Supply Security Focus":
        default_weights = (40, 10, 10, 15, 25)
    elif preset == "Market Opportunity Focus":
        default_weights = (15, 35, 10, 25, 15)
    elif preset == "KC Advantage Focus":
        default_weights = (15, 15, 35, 20, 15)
    else:
        default_weights = (25, 20, 15, 20, 20)

    st.sidebar.markdown("---")

    w_supply = st.sidebar.slider("Supply Risk", 0, 50, default_weights[0], 5,
                                  help="Import dependency & concentration")
    w_market = st.sidebar.slider("Market Opportunity", 0, 50, default_weights[1], 5,
                                  help="Price trends & demand growth")
    w_kc = st.sidebar.slider("KC Advantage", 0, 50, default_weights[2], 5,
                              help="Kansas City logistics benefits")
    w_feasibility = st.sidebar.slider("Production Feasibility", 0, 50, default_weights[3], 5,
                                       help="Domestic production readiness")
    w_strategic = st.sidebar.slider("Strategic Alignment", 0, 50, default_weights[4], 5,
                                     help="DOE & national priorities")

    total_weight = w_supply + w_market + w_kc + w_feasibility + w_strategic

    if total_weight != 100:
        st.sidebar.error(f"⚠️ Weights sum to {total_weight}%. Must equal 100%.")
        weights_valid = False
    else:
        st.sidebar.success("✓ Weights sum to 100%")
        weights_valid = True

    # Show current weights
    st.subheader("Current Weight Configuration")

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Supply Risk", f"{w_supply}%")
    col2.metric("Market Opp.", f"{w_market}%")
    col3.metric("KC Advantage", f"{w_kc}%")
    col4.metric("Feasibility", f"{w_feasibility}%")
    col5.metric("Strategic", f"{w_strategic}%")

    st.markdown("---")

    if weights_valid:
        # Recalculate composite scores with new weights
        df_calc = df.copy()
        df_calc['new_composite'] = (
            df_calc['supply_risk_score'] * (w_supply / 100) +
            df_calc['market_opportunity_score'] * (w_market / 100) +
            df_calc['kc_advantage_score'] * (w_kc / 100) +
            df_calc['production_feasibility_score'] * (w_feasibility / 100) +
            df_calc['strategic_alignment_score'] * (w_strategic / 100)
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
                "supply_risk_score", "market_opportunity_score", "kc_advantage_score",
                "production_feasibility_score", "strategic_alignment_score", "rank_change"
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
                    "market_opportunity_score": "{:.1f}",
                    "kc_advantage_score": "{:.1f}",
                    "production_feasibility_score": "{:.1f}",
                    "strategic_alignment_score": "{:.1f}",
                }),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "new_rank": "Rank",
                    "material": "Material",
                    "new_composite": "Score",
                    "supply_risk_score": "Supply",
                    "market_opportunity_score": "Market",
                    "kc_advantage_score": "KC",
                    "production_feasibility_score": "Feasibility",
                    "strategic_alignment_score": "Strategic",
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

        factors = ['supply_risk_score', 'market_opportunity_score', 'kc_advantage_score',
                   'production_feasibility_score', 'strategic_alignment_score']
        factor_names = ['Supply Risk', 'Market Opportunity', 'KC Advantage',
                        'Production Feasibility', 'Strategic Alignment']

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
