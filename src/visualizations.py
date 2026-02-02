"""Visualization functions for Materials Priority Tool.

This module generates Plotly charts for the Streamlit dashboard:
- Composite score bar chart
- Radar/spider chart for material comparison
- Criticality matrix scatter plot
- Price history line charts
- Import dependency bar chart
- KC hub map
"""

from typing import Optional

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from src import MATERIALS_LIST


# Color scheme for materials
MATERIAL_COLORS = {
    "Lithium": "#1f77b4",
    "Cobalt": "#ff7f0e",
    "Nickel": "#2ca02c",
    "Graphite": "#d62728",
    "Rare Earths": "#9467bd",
    "Manganese": "#8c564b",
}

# Category colors
CATEGORY_COLORS = {
    "Battery": "#1f77b4",
    "Magnet": "#9467bd",
}


def create_composite_score_bar_chart(
    scores_df: pd.DataFrame,
    title: str = "Critical Materials Priority Ranking",
) -> go.Figure:
    """Create horizontal bar chart of composite scores.

    Args:
        scores_df: DataFrame with 'material' and 'composite_score' columns
        title: Chart title

    Returns:
        Plotly Figure object
    """
    df = scores_df.sort_values("composite_score", ascending=True)

    colors = [MATERIAL_COLORS.get(m, "#636EFA") for m in df["material"]]

    fig = go.Figure(
        go.Bar(
            x=df["composite_score"],
            y=df["material"],
            orientation="h",
            marker_color=colors,
            text=df["composite_score"].round(1),
            textposition="outside",
        )
    )

    fig.update_layout(
        title=title,
        xaxis_title="Composite Score",
        yaxis_title="Material",
        xaxis=dict(range=[0, 10]),
        height=400,
        margin=dict(l=100, r=50, t=50, b=50),
    )

    return fig


def create_radar_chart(
    scores_df: pd.DataFrame,
    materials: list[str],
    title: str = "Material Comparison",
) -> go.Figure:
    """Create radar/spider chart comparing materials across all factors.

    Args:
        scores_df: DataFrame with score columns for each factor
        materials: List of materials to include in comparison
        title: Chart title

    Returns:
        Plotly Figure object
    """
    categories = [
        "Supply Risk",
        "Market Opportunity",
        "KC Advantage",
        "Production Feasibility",
        "Strategic Alignment",
    ]

    score_columns = [
        "supply_risk",
        "market_opportunity",
        "kc_advantage",
        "production_feasibility",
        "strategic_alignment",
    ]

    fig = go.Figure()

    for material in materials:
        row = scores_df[scores_df["material"] == material]
        if row.empty:
            continue

        values = [row[col].values[0] for col in score_columns]
        values.append(values[0])  # Close the polygon

        fig.add_trace(
            go.Scatterpolar(
                r=values,
                theta=categories + [categories[0]],
                name=material,
                line_color=MATERIAL_COLORS.get(material, "#636EFA"),
                fill="toself",
                opacity=0.6,
            )
        )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 10]),
        ),
        showlegend=True,
        title=title,
        height=500,
    )

    return fig


def create_criticality_matrix(
    df: pd.DataFrame,
    x_col: str = "supply_risk",
    y_col: str = "strategic_alignment",
    title: str = "Criticality Matrix",
) -> go.Figure:
    """Create scatter plot criticality matrix (DOE-style).

    Args:
        df: DataFrame with material scores
        x_col: Column for x-axis (default: supply_risk)
        y_col: Column for y-axis (default: strategic_alignment)
        title: Chart title

    Returns:
        Plotly Figure object
    """
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        text="material",
        color="material",
        color_discrete_map=MATERIAL_COLORS,
        title=title,
    )

    fig.update_traces(
        textposition="top center",
        marker=dict(size=15),
    )

    fig.update_layout(
        xaxis_title="Supply Risk Score",
        yaxis_title="Strategic Importance Score",
        xaxis=dict(range=[0, 10]),
        yaxis=dict(range=[0, 10]),
        height=500,
        showlegend=False,
    )

    # Add quadrant lines
    fig.add_hline(y=5, line_dash="dash", line_color="gray", opacity=0.5)
    fig.add_vline(x=5, line_dash="dash", line_color="gray", opacity=0.5)

    # Add quadrant labels
    fig.add_annotation(x=7.5, y=7.5, text="Critical", showarrow=False, font=dict(size=12, color="red"))
    fig.add_annotation(x=2.5, y=7.5, text="Important", showarrow=False, font=dict(size=12, color="orange"))
    fig.add_annotation(x=7.5, y=2.5, text="Vulnerable", showarrow=False, font=dict(size=12, color="orange"))
    fig.add_annotation(x=2.5, y=2.5, text="Lower Priority", showarrow=False, font=dict(size=12, color="green"))

    return fig


def create_price_history_chart(
    price_df: pd.DataFrame,
    materials: Optional[list[str]] = None,
    title: str = "Historical Price Trends",
) -> go.Figure:
    """Create multi-line chart of price history.

    Args:
        price_df: DataFrame with 'date', 'material', 'price' columns
        materials: Optional list of materials to include
        title: Chart title

    Returns:
        Plotly Figure object
    """
    if materials:
        price_df = price_df[price_df["material"].isin(materials)]

    fig = px.line(
        price_df,
        x="date",
        y="price",
        color="material",
        color_discrete_map=MATERIAL_COLORS,
        title=title,
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        height=400,
        xaxis=dict(
            rangeselector=dict(
                buttons=list(
                    [
                        dict(count=1, label="1Y", step="year", stepmode="backward"),
                        dict(count=5, label="5Y", step="year", stepmode="backward"),
                        dict(step="all", label="All"),
                    ]
                )
            ),
            rangeslider=dict(visible=True),
        ),
    )

    return fig


def create_import_dependency_chart(
    df: pd.DataFrame,
    title: str = "Import Reliance by Material",
) -> go.Figure:
    """Create bar chart showing import dependency percentages.

    Args:
        df: DataFrame with 'material' and 'import_reliance' columns
        title: Chart title

    Returns:
        Plotly Figure object
    """
    df_sorted = df.sort_values("import_reliance", ascending=True)

    colors = [MATERIAL_COLORS.get(m, "#636EFA") for m in df_sorted["material"]]

    fig = go.Figure(
        go.Bar(
            x=df_sorted["import_reliance"],
            y=df_sorted["material"],
            orientation="h",
            marker_color=colors,
            text=df_sorted["import_reliance"].apply(lambda x: f"{x}%"),
            textposition="outside",
        )
    )

    fig.update_layout(
        title=title,
        xaxis_title="Net Import Reliance (%)",
        yaxis_title="Material",
        xaxis=dict(range=[0, 105]),
        height=400,
    )

    return fig


def create_summary_cards_data(scores_df: pd.DataFrame) -> list[dict]:
    """Prepare data for summary cards display.

    Args:
        scores_df: DataFrame with material scores

    Returns:
        List of dictionaries with card data for each material
    """
    cards = []
    for _, row in scores_df.iterrows():
        cards.append(
            {
                "material": row["material"],
                "rank": int(row["rank"]),
                "composite_score": round(row["composite_score"], 1),
                "top_factor": _get_top_factor(row),
                "color": MATERIAL_COLORS.get(row["material"], "#636EFA"),
            }
        )
    return cards


def _get_top_factor(row: pd.Series) -> str:
    """Get the highest-scoring factor for a material."""
    factors = {
        "Supply Risk": row.get("supply_risk", 0),
        "Market Opportunity": row.get("market_opportunity", 0),
        "KC Advantage": row.get("kc_advantage", 0),
        "Production Feasibility": row.get("production_feasibility", 0),
        "Strategic Alignment": row.get("strategic_alignment", 0),
    }
    return max(factors, key=factors.get)
