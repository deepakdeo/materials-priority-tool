"""Priority Rankings Page - Composite scores and material rankings."""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.utils import export_to_csv, export_to_excel, generate_pdf_report

st.set_page_config(page_title="Priority Rankings", page_icon="📊", layout="wide")

st.title("📊 Priority Rankings")
st.markdown("Composite scores and rankings for critical materials based on 5-factor analysis.")

# Data paths
DATA_DIR = Path(__file__).parent.parent / "data"
PROCESSED_DIR = DATA_DIR / "processed"


@st.cache_data
def load_materials_data():
    """Load processed materials data with scores."""
    filepath = PROCESSED_DIR / "materials_master.csv"
    if filepath.exists():
        return pd.read_csv(filepath)
    return None


# Color scheme for materials
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

# Load data
df = load_materials_data()

if df is not None:
    # Sort by rank
    df = df.sort_values('rank')

    # Display rankings table
    st.subheader("Material Rankings")

    display_cols = [
        "rank", "material", "primary_use", "composite_score",
        "supply_risk_score", "market_opportunity_score", "kc_advantage_score",
        "production_feasibility_score", "strategic_alignment_score",
        "criticality_category"
    ]

    st.dataframe(
        df[display_cols].style.format({
            "composite_score": "{:.2f}",
            "supply_risk_score": "{:.1f}",
            "market_opportunity_score": "{:.1f}",
            "kc_advantage_score": "{:.1f}",
            "production_feasibility_score": "{:.1f}",
            "strategic_alignment_score": "{:.1f}",
        }).background_gradient(subset=['composite_score'], cmap='RdYlGn'),
        width="stretch",
        hide_index=True,
    )

    # Export buttons
    st.subheader("Export Data")
    export_cols = st.columns(3)

    with export_cols[0]:
        csv_data = export_to_csv(df)
        st.download_button(
            label="📄 Download CSV",
            data=csv_data,
            file_name="materials_priority_rankings.csv",
            mime="text/csv",
        )

    with export_cols[1]:
        excel_data = export_to_excel(df, "Priority Rankings")
        st.download_button(
            label="📊 Download Excel",
            data=excel_data,
            file_name="materials_priority_rankings.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    with export_cols[2]:
        pdf_data = generate_pdf_report(df)
        st.download_button(
            label="📑 Download PDF Report",
            data=pdf_data,
            file_name="materials_priority_report.pdf",
            mime="application/pdf",
        )

    st.markdown("---")

    # Two column layout for charts
    col1, col2 = st.columns(2)

    with col1:
        # Composite Score Bar Chart
        st.subheader("Composite Score Comparison")

        df_sorted = df.sort_values('composite_score', ascending=True)
        colors = [MATERIAL_COLORS.get(m, "#636EFA") for m in df_sorted['material']]

        fig_bar = go.Figure(go.Bar(
            x=df_sorted['composite_score'],
            y=df_sorted['material'],
            orientation='h',
            marker_color=colors,
            text=df_sorted['composite_score'].round(2),
            textposition='outside',
        ))

        fig_bar.update_layout(
            xaxis_title="Composite Score",
            yaxis_title="",
            xaxis=dict(range=[0, 10]),
            height=400,
            margin=dict(l=100, r=50, t=20, b=50),
        )

        st.plotly_chart(fig_bar, use_container_width=True)

    with col2:
        # Radar Chart for Top 3
        st.subheader("Top 3 Materials Comparison")

        categories = [
            'Supply Risk', 'Market Opportunity', 'KC Advantage',
            'Production Feasibility', 'Strategic Alignment'
        ]
        score_cols = [
            'supply_risk_score', 'market_opportunity_score', 'kc_advantage_score',
            'production_feasibility_score', 'strategic_alignment_score'
        ]

        fig_radar = go.Figure()

        for _, row in df.head(3).iterrows():
            values = [row[col] for col in score_cols]
            values.append(values[0])  # Close the polygon

            fig_radar.add_trace(go.Scatterpolar(
                r=values,
                theta=categories + [categories[0]],
                name=row['material'],
                line_color=MATERIAL_COLORS.get(row['material'], "#636EFA"),
                fill='toself',
                opacity=0.6,
            ))

        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 10])),
            showlegend=True,
            height=400,
            margin=dict(l=50, r=50, t=20, b=50),
        )

        st.plotly_chart(fig_radar, use_container_width=True)

    st.markdown("---")

    # Summary cards
    st.subheader("Top 3 Priority Materials")

    cols = st.columns(3)
    for i, (_, row) in enumerate(df.head(3).iterrows()):
        with cols[i]:
            st.metric(
                label=f"#{int(row['rank'])} {row['material']}",
                value=f"{row['composite_score']:.2f}",
                delta=row["criticality_category"],
            )
            st.caption(f"Top producer: {row['top_producer']} ({row['top_producer_share_pct']}%)")
            st.caption(f"Import reliance: {row['import_reliance_pct']}%")

    st.markdown("---")

    # Score Breakdown Stacked Bar Chart
    st.subheader("Score Breakdown by Factor")
    st.caption("Contribution of each factor to composite score (weighted)")

    # Calculate weighted contributions
    weights = {"Supply Risk": 0.25, "Market Opp.": 0.20, "KC Advantage": 0.15,
               "Feasibility": 0.20, "Strategic": 0.20}

    breakdown_data = []
    for _, row in df.iterrows():
        breakdown_data.append({
            "Material": row["material"],
            "Supply Risk": row["supply_risk_score"] * weights["Supply Risk"],
            "Market Opp.": row["market_opportunity_score"] * weights["Market Opp."],
            "KC Advantage": row["kc_advantage_score"] * weights["KC Advantage"],
            "Feasibility": row["production_feasibility_score"] * weights["Feasibility"],
            "Strategic": row["strategic_alignment_score"] * weights["Strategic"],
        })

    breakdown_df = pd.DataFrame(breakdown_data)
    breakdown_df = breakdown_df.set_index("Material")

    fig_stacked = go.Figure()
    colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
    for i, col in enumerate(breakdown_df.columns):
        fig_stacked.add_trace(go.Bar(
            name=col,
            y=breakdown_df.index,
            x=breakdown_df[col],
            orientation='h',
            marker_color=colors[i],
        ))

    fig_stacked.update_layout(
        barmode='stack',
        xaxis_title="Weighted Score Contribution",
        yaxis_title="",
        height=350,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
        margin=dict(l=100, r=50, t=50, b=50),
    )

    st.plotly_chart(fig_stacked, use_container_width=True)

    st.markdown("---")

    # Criticality Matrix
    st.subheader("Criticality Matrix")
    st.caption("Materials positioned by Supply Risk vs Strategic Alignment")

    fig_matrix = px.scatter(
        df,
        x='supply_risk_score',
        y='strategic_alignment_score',
        text='material',
        color='material',
        color_discrete_map=MATERIAL_COLORS,
        size='composite_score',
        size_max=30,
    )

    fig_matrix.update_traces(textposition='top center')

    fig_matrix.update_layout(
        xaxis_title="Supply Risk Score",
        yaxis_title="Strategic Alignment Score",
        xaxis=dict(range=[0, 10]),
        yaxis=dict(range=[0, 10]),
        height=500,
        showlegend=False,
    )

    # Add quadrant lines and labels
    fig_matrix.add_hline(y=5, line_dash="dash", line_color="gray", opacity=0.5)
    fig_matrix.add_vline(x=5, line_dash="dash", line_color="gray", opacity=0.5)

    fig_matrix.add_annotation(x=7.5, y=9, text="Critical Priority", showarrow=False,
                               font=dict(size=11, color="darkred"))
    fig_matrix.add_annotation(x=2.5, y=9, text="Strategic Focus", showarrow=False,
                               font=dict(size=11, color="darkorange"))
    fig_matrix.add_annotation(x=7.5, y=1.5, text="Supply Vulnerable", showarrow=False,
                               font=dict(size=11, color="darkorange"))
    fig_matrix.add_annotation(x=2.5, y=1.5, text="Lower Priority", showarrow=False,
                               font=dict(size=11, color="darkgreen"))

    st.plotly_chart(fig_matrix, use_container_width=True)

    # Data timestamp
    st.markdown("---")
    st.caption("Data sources: USGS Mineral Commodity Summaries, DOE Critical Materials Assessment, World Bank")

else:
    st.error("Processed data not found. Please run the data processor first.")
    st.code("python -m src.data_processor", language="bash")
