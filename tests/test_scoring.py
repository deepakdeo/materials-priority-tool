"""Tests for the scoring module."""

import pytest
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scoring import (
    calculate_supply_risk_score,
    calculate_market_opportunity_score,
    calculate_kc_advantage_score,
    calculate_production_feasibility_score,
    calculate_strategic_alignment_score,
    calculate_composite_score,
)


class TestSupplyRiskScore:
    """Tests for supply risk scoring."""

    def test_high_import_reliance(self):
        """100% import reliance should give high score."""
        score = calculate_supply_risk_score(
            import_reliance=100,
            top_country_share=80,
        )
        assert score >= 7

    def test_low_import_reliance(self):
        """Low import reliance should give lower score."""
        score = calculate_supply_risk_score(
            import_reliance=20,
            top_country_share=30,
        )
        assert score <= 5

    def test_score_bounds(self):
        """Score should be between 1 and 10."""
        score = calculate_supply_risk_score(100, 100, 10000)
        assert 1 <= score <= 10

        score = calculate_supply_risk_score(0, 0, 0)
        assert 1 <= score <= 10


class TestMarketOpportunityScore:
    """Tests for market opportunity scoring."""

    def test_high_growth(self):
        """High price and demand growth should score high."""
        score = calculate_market_opportunity_score(
            price_growth_5yr=100,
            demand_growth_projection=20,
            market_size_bn=10,
        )
        assert score >= 7

    def test_negative_growth(self):
        """Negative price growth should score lower."""
        score = calculate_market_opportunity_score(
            price_growth_5yr=-20,
            demand_growth_projection=5,
            market_size_bn=5,
        )
        assert score <= 6

    def test_score_bounds(self):
        """Score should be between 1 and 10."""
        score = calculate_market_opportunity_score(200, 50, 100)
        assert 1 <= score <= 10


class TestKCAdvantageScore:
    """Tests for KC advantage scoring."""

    def test_high_advantage(self):
        """All high values should give high score."""
        score = calculate_kc_advantage_score(
            bulk_transport_benefit=9,
            central_location_benefit=9,
            existing_infrastructure=8,
        )
        assert score >= 8

    def test_low_advantage(self):
        """Low values should give low score."""
        score = calculate_kc_advantage_score(
            bulk_transport_benefit=3,
            central_location_benefit=3,
            existing_infrastructure=2,
        )
        assert score <= 4


class TestProductionFeasibilityScore:
    """Tests for production feasibility scoring."""

    def test_existing_production(self):
        """Existing domestic production should boost score."""
        score_with = calculate_production_feasibility_score(
            domestic_production_exists=True,
            technology_readiness=7,
            capex_intensity=5,
        )
        score_without = calculate_production_feasibility_score(
            domestic_production_exists=False,
            technology_readiness=7,
            capex_intensity=5,
        )
        assert score_with > score_without


class TestStrategicAlignmentScore:
    """Tests for strategic alignment scoring."""

    def test_critical_material(self):
        """Critical materials (DOE 4/4) should score high."""
        score = calculate_strategic_alignment_score(
            doe_importance=4,
            doe_supply_risk=4,
            battery_relevance=9,
            defense_relevance=5,
        )
        assert score >= 7


class TestCompositeScore:
    """Tests for composite score calculation."""

    def test_default_weights(self):
        """Composite with default weights should work."""
        scores = {
            "supply_risk": 7,
            "market_opportunity": 6,
            "kc_advantage": 8,
            "production_feasibility": 5,
            "strategic_alignment": 7,
        }
        composite = calculate_composite_score(scores)
        assert 1 <= composite <= 10

    def test_custom_weights(self):
        """Custom weights should change result."""
        scores = {
            "supply_risk": 10,
            "market_opportunity": 1,
            "kc_advantage": 1,
            "production_feasibility": 1,
            "strategic_alignment": 1,
        }

        # Heavy supply risk weight
        weights_supply = {
            "supply_risk": 0.8,
            "market_opportunity": 0.05,
            "kc_advantage": 0.05,
            "production_feasibility": 0.05,
            "strategic_alignment": 0.05,
        }

        # Heavy market weight
        weights_market = {
            "supply_risk": 0.05,
            "market_opportunity": 0.8,
            "kc_advantage": 0.05,
            "production_feasibility": 0.05,
            "strategic_alignment": 0.05,
        }

        composite_supply = calculate_composite_score(scores, weights_supply)
        composite_market = calculate_composite_score(scores, weights_market)

        assert composite_supply > composite_market

    def test_invalid_weights(self):
        """Weights not summing to 1.0 should raise error."""
        scores = {"supply_risk": 5, "market_opportunity": 5, "kc_advantage": 5,
                  "production_feasibility": 5, "strategic_alignment": 5}
        weights = {"supply_risk": 0.5, "market_opportunity": 0.5, "kc_advantage": 0.5,
                   "production_feasibility": 0.5, "strategic_alignment": 0.5}

        with pytest.raises(ValueError):
            calculate_composite_score(scores, weights)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
