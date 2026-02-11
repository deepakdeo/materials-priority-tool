"""Uncertainty Analysis Page - Monte Carlo simulation for ranking confidence."""

import sys
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.tour import render_tour_widget
from src.auth import check_password, render_logout_button
from src.theme import render_theme_toggle, apply_theme_css
from src.feedback import render_feedback_widget

st.set_page_config(page_title="Uncertainty Analysis", page_icon="🎲", layout="wide")

# Check authentication
if not check_password():
    st.stop()

render_logout_button()
render_theme_toggle()
render_feedback_widget()
apply_theme_css()

# Render tour widget if active
render_tour_widget()

st.title("🎲 Uncertainty Analysis")
st.markdown("Monte Carlo simulation to understand ranking confidence under data uncertainty.")

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
    # Expandable explanation section
    with st.expander("📖 **What is this page for?** Click to learn more", expanded=False):
        st.markdown("""
        ## Why Uncertainty Analysis Matters

        Our rankings show Rare Earths as #1 and Gallium as #2. But **how confident should you be** in these rankings?

        Real-world data isn't perfect:
        - Import reliance figures are estimates that could be off by 5-10%
        - DOE assessments may change as conditions evolve
        - Some materials have scores very close together

        **The key question:** If the underlying data shifted slightly, would the rankings change?

        ---

        ## What is Monte Carlo Simulation?

        Instead of calculating rankings once, Monte Carlo simulation:

        1. **Runs thousands of "what-if" scenarios** (e.g., 1,000 times)
        2. **Each time, it slightly randomizes the scores** within the uncertainty ranges you set
        3. **Recalculates the rankings** for each scenario
        4. **Counts how often each material finishes #1, #2, etc.**

        ---

        ## How to Interpret Results

        | If a material is #1 in... | Confidence Level | What it means |
        |---------------------------|------------------|---------------|
        | **>80% of simulations** | High | Very robust ranking — unlikely to change |
        | **50-80% of simulations** | Medium | Reasonably confident, but close competitors |
        | **<50% of simulations** | Low | Close call — small data changes could flip rankings |

        ---

        ## Practical Example

        - **Rare Earths (8.84)** vs **Gallium (8.76)** — only 0.08 points apart
          - Monte Carlo might show they swap places in 15% of scenarios
          - This tells you: "These two are essentially tied for priority"

        - **Rare Earths (8.84)** vs **Copper (5.36)** — 3.48 points apart
          - Monte Carlo will show Copper never beats Rare Earths
          - This tells you: "Rare Earths is definitively higher priority than Copper"

        ---

        ## When to Use This

        - **Before making investment decisions** — Know which rankings are "sure things" vs "close calls"
        - **When presenting to stakeholders** — Show confidence intervals, not just point estimates
        - **When data quality is uncertain** — Test how sensitive rankings are to data errors
        """)

    st.markdown("""
    ### Quick Summary

    This page tests **how robust your rankings are**. It runs thousands of scenarios with slightly
    randomized scores to see how often each material maintains its rank. High confidence (>80%)
    means the ranking is solid. Low confidence (<50%) means it's a close call.
    """)

    st.markdown("---")

    # Sidebar controls
    st.sidebar.header("Simulation Settings")

    st.sidebar.markdown("**Step 1: Choose simulation count**")
    n_simulations = st.sidebar.slider(
        "Number of simulations",
        min_value=100,
        max_value=5000,
        value=1000,
        step=100,
        help="More simulations = more accurate results. 1,000 is a good balance."
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Step 2: Set uncertainty ranges**")
    st.sidebar.caption("How much could each score realistically vary? Higher = more uncertainty.")

    uncertainty_supply = st.sidebar.slider(
        "Supply Risk (±%)",
        min_value=0,
        max_value=30,
        value=10,
        help="Example: ±10% means a score of 8.0 could range from 7.2 to 8.8"
    )

    uncertainty_strategic = st.sidebar.slider(
        "Strategic Alignment (±%)",
        min_value=0,
        max_value=30,
        value=10,
        help="DOE categories are fairly stable, so 10% is reasonable"
    )

    uncertainty_feasibility = st.sidebar.slider(
        "Production Feasibility (±%)",
        min_value=0,
        max_value=30,
        value=15,
        help="Binary (yes/no) converted to scores, so moderate uncertainty"
    )

    # Weights (3-factor model)
    st.sidebar.markdown("---")
    st.sidebar.subheader("Scoring Weights (3-Factor Model)")

    w_supply = st.sidebar.number_input("Supply Risk %", 0, 100, 40)
    w_strategic = st.sidebar.number_input("Strategic Alignment %", 0, 100, 40)
    w_feasibility = st.sidebar.number_input("Production Feasibility %", 0, 100, 20)

    total_weight = w_supply + w_strategic + w_feasibility

    if total_weight != 100:
        st.sidebar.error(f"Weights must sum to 100% (currently {total_weight}%)")
        weights_valid = False
    else:
        st.sidebar.success("✓ Weights valid")
        weights_valid = True

    if weights_valid:
        # Run simulation button
        if st.button("🎲 Run Monte Carlo Simulation", type="primary"):

            with st.spinner(f"Running {n_simulations} simulations..."):

                # Store results
                all_rankings = []
                all_scores = {mat: [] for mat in df['material'].tolist()}

                # Progress bar
                progress_bar = st.progress(0)

                for i in range(n_simulations):
                    # Create perturbed data
                    sim_df = df.copy()

                    # Add noise to scores based on uncertainty settings
                    def add_noise(value, uncertainty_pct, min_val=1, max_val=10):
                        noise = np.random.normal(0, uncertainty_pct / 100 * value)
                        return np.clip(value + noise, min_val, max_val)

                    # Perturb factor scores (3-factor model)
                    sim_df['supply_risk_score'] = sim_df['supply_risk_score'].apply(
                        lambda x: add_noise(x, uncertainty_supply))
                    sim_df['strategic_alignment_score'] = sim_df['strategic_alignment_score'].apply(
                        lambda x: add_noise(x, uncertainty_strategic))
                    sim_df['production_feasibility_score'] = sim_df['production_feasibility_score'].apply(
                        lambda x: add_noise(x, uncertainty_feasibility))

                    # Calculate composite scores (3-factor model)
                    sim_df['sim_composite'] = (
                        sim_df['supply_risk_score'] * (w_supply / 100) +
                        sim_df['strategic_alignment_score'] * (w_strategic / 100) +
                        sim_df['production_feasibility_score'] * (w_feasibility / 100)
                    )

                    # Record rankings
                    sim_df['sim_rank'] = sim_df['sim_composite'].rank(ascending=False, method='min')
                    rankings = sim_df.set_index('material')['sim_rank'].to_dict()
                    all_rankings.append(rankings)

                    # Record scores
                    for mat in df['material'].tolist():
                        score = sim_df[sim_df['material'] == mat]['sim_composite'].iloc[0]
                        all_scores[mat].append(score)

                    # Update progress
                    if i % 50 == 0:
                        progress_bar.progress(i / n_simulations)

                progress_bar.progress(1.0)

            st.success(f"✓ Completed {n_simulations} simulations")

            st.markdown("---")

            # Analyze results
            rankings_df = pd.DataFrame(all_rankings)

            # Probability of each rank
            st.subheader("Ranking Probability Distribution")
            st.markdown("How often does each material achieve each rank?")

            prob_matrix = pd.DataFrame()
            for mat in df['material'].tolist():
                probs = rankings_df[mat].value_counts(normalize=True).sort_index()
                prob_matrix[mat] = probs

            prob_matrix = prob_matrix.fillna(0).T
            prob_matrix.columns = [f"Rank {int(c)}" for c in prob_matrix.columns]

            # Heatmap
            fig_heatmap = go.Figure(data=go.Heatmap(
                z=prob_matrix.values * 100,
                x=prob_matrix.columns,
                y=prob_matrix.index,
                colorscale='Blues',
                text=np.round(prob_matrix.values * 100, 1),
                texttemplate='%{text}%',
                textfont={"size": 10},
                hoverongaps=False,
                colorbar=dict(title="Probability %"),
            ))

            fig_heatmap.update_layout(
                title="Probability of Achieving Each Rank (%)",
                xaxis_title="Rank",
                yaxis_title="Material",
                height=450,
            )

            st.plotly_chart(fig_heatmap, use_container_width=True)

            st.markdown("---")

            # Top rank probability
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Probability of Being #1")

                top_probs = rankings_df.apply(lambda x: (x == 1).mean()).sort_values(ascending=True)
                colors = [MATERIAL_COLORS.get(m, "#636EFA") for m in top_probs.index]

                fig_top = go.Figure(go.Bar(
                    x=top_probs.values * 100,
                    y=top_probs.index,
                    orientation='h',
                    marker_color=colors,
                    text=[f"{p:.1f}%" for p in top_probs.values * 100],
                    textposition='outside',
                ))

                fig_top.update_layout(
                    xaxis_title="Probability (%)",
                    yaxis_title="",
                    xaxis=dict(range=[0, 100]),
                    height=400,
                    margin=dict(l=100, r=50, t=20, b=50),
                )

                st.plotly_chart(fig_top, use_container_width=True)

            with col2:
                st.subheader("Score Distribution (Box Plot)")

                score_data = []
                for mat, scores in all_scores.items():
                    for s in scores:
                        score_data.append({"Material": mat, "Score": s})

                score_df = pd.DataFrame(score_data)

                fig_box = px.box(
                    score_df,
                    x="Material",
                    y="Score",
                    color="Material",
                    color_discrete_map=MATERIAL_COLORS,
                )

                fig_box.update_layout(
                    showlegend=False,
                    height=400,
                    yaxis_title="Composite Score",
                    xaxis_title="",
                )

                st.plotly_chart(fig_box, use_container_width=True)

            st.markdown("---")

            # Summary statistics
            st.subheader("Summary Statistics")

            summary_data = []
            for mat in df['material'].tolist():
                scores = all_scores[mat]
                ranks = rankings_df[mat].tolist()

                summary_data.append({
                    "Material": mat,
                    "Mean Score": f"{np.mean(scores):.2f}",
                    "Score Std Dev": f"{np.std(scores):.2f}",
                    "95% CI": f"[{np.percentile(scores, 2.5):.2f}, {np.percentile(scores, 97.5):.2f}]",
                    "Median Rank": f"{np.median(ranks):.0f}",
                    "P(Top 3)": f"{sum(r <= 3 for r in ranks) / len(ranks) * 100:.1f}%",
                    "P(#1)": f"{sum(r == 1 for r in ranks) / len(ranks) * 100:.1f}%",
                })

            summary_df = pd.DataFrame(summary_data)
            st.dataframe(summary_df, use_container_width=True, hide_index=True)

            st.markdown("---")

            # Key insights
            st.subheader("Key Insights")

            # Find most likely #1
            top_probs = rankings_df.apply(lambda x: (x == 1).mean())
            most_likely_top = top_probs.idxmax()
            top_prob = top_probs.max() * 100

            # Find most uncertain material
            score_stds = {mat: np.std(scores) for mat, scores in all_scores.items()}
            most_uncertain = max(score_stds, key=score_stds.get)

            # Find materials that could swap
            runner_up = top_probs.nlargest(2).index[1]
            runner_up_prob = top_probs.nlargest(2).iloc[1] * 100

            st.markdown(f"""
            - **Most likely #1:** {most_likely_top} ({top_prob:.1f}% probability)
            - **Runner up:** {runner_up} ({runner_up_prob:.1f}% probability of being #1)
            - **Most uncertain:** {most_uncertain} (highest score variability)
            - **Confidence:** {'High' if top_prob > 70 else 'Medium' if top_prob > 50 else 'Low'}
              confidence in top ranking ({'>' if top_prob > 70 else '50-70%' if top_prob > 50 else '<50%'})
            """)

            if top_prob < 50:
                st.warning(f"""
                ⚠️ **Ranking uncertainty is high.** {most_likely_top} is the most likely #1,
                but there's a {100 - top_prob:.1f}% chance another material could take the top spot.
                Consider reducing input uncertainty or gathering better data.
                """)

    st.markdown("---")
    st.caption("Monte Carlo simulation uses random sampling to estimate ranking confidence intervals.")

else:
    st.error("Processed data not found. Please run the data processor first.")
    st.code("python -m src.data_processor", language="bash")
