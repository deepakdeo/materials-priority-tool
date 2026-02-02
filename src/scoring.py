"""Scoring engine for Materials Priority Tool.

This module implements the 5-factor scoring methodology:
1. Supply Risk Score (25%) — Import dependency, geographic concentration
2. Market Opportunity Score (20%) — Price trends, demand growth
3. KC Advantage Score (15%) — Kansas City logistics benefits
4. Production Feasibility Score (20%) — Domestic production maturity
5. Strategic Alignment Score (20%) — DOE criticality, battery/EV alignment

All scores are normalized to 1-10 scale.
"""

from typing import Optional

import numpy as np
import pandas as pd

from src import DEFAULT_WEIGHTS, MATERIALS_LIST


def calculate_supply_risk_score(
    import_reliance: float,
    top_country_share: float,
    hhi_concentration: Optional[float] = None,
) -> float:
    """Calculate supply risk score based on import dependency and concentration.

    Args:
        import_reliance: Net import reliance as percentage (0-100)
        top_country_share: Share of production from top producing country (0-100)
        hhi_concentration: Optional Herfindahl-Hirschman Index (0-10000)

    Returns:
        Supply risk score (1-10, higher = more risk = higher priority)
    """
    # Normalize import reliance to 0-5 scale
    import_score = (import_reliance / 100) * 5

    # Normalize top country share to 0-3 scale
    concentration_score = (top_country_share / 100) * 3

    # Add HHI component if available (0-2 scale)
    if hhi_concentration is not None:
        hhi_score = min(hhi_concentration / 5000, 1) * 2
    else:
        hhi_score = 0

    total = import_score + concentration_score + hhi_score
    return min(max(total, 1), 10)


def calculate_market_opportunity_score(
    price_growth_5yr: float,
    demand_growth_projection: float,
    market_size_bn: float,
) -> float:
    """Calculate market opportunity score based on price and demand trends.

    Args:
        price_growth_5yr: 5-year price growth percentage
        demand_growth_projection: Projected annual demand growth percentage
        market_size_bn: Market size in billions USD

    Returns:
        Market opportunity score (1-10, higher = better opportunity)
    """
    # Price growth component (0-4 scale, cap at 100% growth)
    price_score = min(max(price_growth_5yr, 0), 100) / 25

    # Demand growth component (0-4 scale, assume max 20% annual growth)
    demand_score = min(max(demand_growth_projection, 0), 20) / 5

    # Market size component (0-2 scale, log scale for large markets)
    size_score = min(np.log10(max(market_size_bn, 0.1) + 1), 2)

    total = price_score + demand_score + size_score
    return min(max(total, 1), 10)


def calculate_kc_advantage_score(
    bulk_transport_benefit: float,
    central_location_benefit: float,
    existing_infrastructure: float,
) -> float:
    """Calculate Kansas City logistics advantage score.

    Args:
        bulk_transport_benefit: Benefit from rail/river transport (1-10)
        central_location_benefit: Benefit from central US location (1-10)
        existing_infrastructure: Existing processing/storage infrastructure (1-10)

    Returns:
        KC advantage score (1-10, higher = better fit for KC)
    """
    # Weighted average of KC-specific factors
    score = (
        bulk_transport_benefit * 0.4
        + central_location_benefit * 0.35
        + existing_infrastructure * 0.25
    )
    return min(max(score, 1), 10)


def calculate_production_feasibility_score(
    domestic_production_exists: bool,
    technology_readiness: float,
    capex_intensity: float,
) -> float:
    """Calculate production feasibility score.

    Args:
        domestic_production_exists: Whether US has any current production
        technology_readiness: Technology readiness level (1-10)
        capex_intensity: Capital intensity (lower = easier, 1-10 scale inverted)

    Returns:
        Production feasibility score (1-10, higher = more feasible)
    """
    # Existing production bonus
    existing_bonus = 2 if domestic_production_exists else 0

    # Technology readiness (0-5 scale)
    tech_score = technology_readiness / 2

    # Inverted capex intensity (0-3 scale, lower capex = higher score)
    capex_score = (11 - capex_intensity) / 3.33

    total = existing_bonus + tech_score + capex_score
    return min(max(total, 1), 10)


def calculate_strategic_alignment_score(
    doe_importance: float,
    doe_supply_risk: float,
    battery_relevance: float,
    defense_relevance: float,
) -> float:
    """Calculate strategic alignment score with DOE and national priorities.

    Args:
        doe_importance: DOE Importance to Energy score (1-4)
        doe_supply_risk: DOE Supply Risk score (1-4)
        battery_relevance: Relevance to battery supply chain (1-10)
        defense_relevance: Relevance to defense applications (1-10)

    Returns:
        Strategic alignment score (1-10, higher = better alignment)
    """
    # DOE criticality composite (0-4 scale)
    doe_composite = (doe_importance + doe_supply_risk) / 2

    # Battery relevance (0-3 scale)
    battery_score = battery_relevance / 3.33

    # Defense relevance (0-2 scale)
    defense_score = defense_relevance / 5

    total = doe_composite + battery_score + defense_score + 1  # +1 to shift range
    return min(max(total, 1), 10)


def calculate_composite_score(
    scores: dict[str, float],
    weights: Optional[dict[str, float]] = None,
) -> float:
    """Calculate weighted composite score from individual factor scores.

    Args:
        scores: Dictionary with keys matching weight keys and float values (1-10)
        weights: Optional custom weights (must sum to 1.0). Uses DEFAULT_WEIGHTS if None.

    Returns:
        Composite score (1-10)
    """
    if weights is None:
        weights = DEFAULT_WEIGHTS

    # Validate weights sum to 1.0
    weight_sum = sum(weights.values())
    if not np.isclose(weight_sum, 1.0, atol=0.01):
        raise ValueError(f"Weights must sum to 1.0, got {weight_sum}")

    composite = sum(scores.get(factor, 0) * weight for factor, weight in weights.items())
    return round(composite, 2)


def score_all_materials(
    materials_df: pd.DataFrame,
    weights: Optional[dict[str, float]] = None,
) -> pd.DataFrame:
    """Score all materials and return ranked DataFrame.

    Args:
        materials_df: DataFrame with scoring input columns for each material
        weights: Optional custom weights for composite calculation

    Returns:
        DataFrame with individual scores, composite score, and rank
    """
    if weights is None:
        weights = DEFAULT_WEIGHTS

    results = []
    for _, row in materials_df.iterrows():
        scores = {
            "supply_risk": row.get("supply_risk_score", 5),
            "market_opportunity": row.get("market_opportunity_score", 5),
            "kc_advantage": row.get("kc_advantage_score", 5),
            "production_feasibility": row.get("production_feasibility_score", 5),
            "strategic_alignment": row.get("strategic_alignment_score", 5),
        }
        composite = calculate_composite_score(scores, weights)
        results.append(
            {
                "material": row["material"],
                **scores,
                "composite_score": composite,
            }
        )

    results_df = pd.DataFrame(results)
    results_df["rank"] = results_df["composite_score"].rank(ascending=False, method="min").astype(int)
    return results_df.sort_values("rank")
