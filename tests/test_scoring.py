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


class TestScoreAllMaterials:
    """Tests for the score_all_materials function."""

    def test_returns_dataframe(self):
        """Should return a pandas DataFrame."""
        from src.scoring import score_all_materials
        import pandas as pd

        df = pd.DataFrame([
            {"material": "TestMaterial", "supply_risk_score": 7, "market_opportunity_score": 6,
             "kc_advantage_score": 5, "production_feasibility_score": 6, "strategic_alignment_score": 7}
        ])
        result = score_all_materials(df)
        assert isinstance(result, pd.DataFrame)

    def test_adds_composite_score(self):
        """Should add composite_score column."""
        from src.scoring import score_all_materials
        import pandas as pd

        df = pd.DataFrame([
            {"material": "TestMaterial", "supply_risk_score": 7, "market_opportunity_score": 6,
             "kc_advantage_score": 5, "production_feasibility_score": 6, "strategic_alignment_score": 7}
        ])
        result = score_all_materials(df)
        assert "composite_score" in result.columns

    def test_adds_rank_column(self):
        """Should add rank column."""
        from src.scoring import score_all_materials
        import pandas as pd

        df = pd.DataFrame([
            {"material": "Material1", "supply_risk_score": 7, "market_opportunity_score": 6,
             "kc_advantage_score": 5, "production_feasibility_score": 6, "strategic_alignment_score": 7},
            {"material": "Material2", "supply_risk_score": 5, "market_opportunity_score": 5,
             "kc_advantage_score": 5, "production_feasibility_score": 5, "strategic_alignment_score": 5}
        ])
        result = score_all_materials(df)
        assert "rank" in result.columns

    def test_ranks_correctly(self):
        """Higher composite scores should get lower rank numbers."""
        from src.scoring import score_all_materials
        import pandas as pd

        df = pd.DataFrame([
            {"material": "HighScore", "supply_risk_score": 9, "market_opportunity_score": 9,
             "kc_advantage_score": 9, "production_feasibility_score": 9, "strategic_alignment_score": 9},
            {"material": "LowScore", "supply_risk_score": 2, "market_opportunity_score": 2,
             "kc_advantage_score": 2, "production_feasibility_score": 2, "strategic_alignment_score": 2}
        ])
        result = score_all_materials(df)
        high_rank = result[result["material"] == "HighScore"]["rank"].iloc[0]
        low_rank = result[result["material"] == "LowScore"]["rank"].iloc[0]
        assert high_rank < low_rank


class TestEdgeCases:
    """Tests for edge cases and boundary conditions."""

    def test_zero_values(self):
        """All zero inputs should still produce valid scores."""
        assert 1 <= calculate_supply_risk_score(0, 0, 0) <= 10
        assert 1 <= calculate_market_opportunity_score(0, 0, 0.1) <= 10
        assert 1 <= calculate_kc_advantage_score(1, 1, 1) <= 10
        assert 1 <= calculate_production_feasibility_score(False, 1, 10) <= 10
        assert 1 <= calculate_strategic_alignment_score(1, 1, 1, 1) <= 10

    def test_maximum_values(self):
        """Maximum inputs should still produce valid scores."""
        assert 1 <= calculate_supply_risk_score(100, 100, 10000) <= 10
        assert 1 <= calculate_market_opportunity_score(200, 50, 100) <= 10
        assert 1 <= calculate_kc_advantage_score(10, 10, 10) <= 10
        assert 1 <= calculate_production_feasibility_score(True, 10, 1) <= 10
        assert 1 <= calculate_strategic_alignment_score(4, 4, 10, 10) <= 10

    def test_negative_price_growth(self):
        """Negative price growth should be handled (clamped to 0)."""
        score = calculate_market_opportunity_score(-50, 10, 5)
        assert 1 <= score <= 10

    def test_weights_close_to_one(self):
        """Weights that sum close to 1.0 (within tolerance) should work."""
        scores = {"supply_risk": 5, "market_opportunity": 5, "kc_advantage": 5,
                  "production_feasibility": 5, "strategic_alignment": 5}
        weights = {"supply_risk": 0.25, "market_opportunity": 0.20, "kc_advantage": 0.15,
                   "production_feasibility": 0.20, "strategic_alignment": 0.20}
        composite = calculate_composite_score(scores, weights)
        assert 1 <= composite <= 10


class TestIntegrationWithData:
    """Integration tests with actual processed data."""

    def test_load_and_score_actual_data(self):
        """Should be able to load and score actual materials data."""
        import pandas as pd
        from pathlib import Path

        data_path = Path(__file__).parent.parent / "data" / "processed" / "materials_master.csv"
        if data_path.exists():
            df = pd.read_csv(data_path)
            assert len(df) == 10  # 10 materials
            assert "composite_score" in df.columns
            assert "rank" in df.columns
            assert df["composite_score"].min() >= 1
            assert df["composite_score"].max() <= 10

    def test_all_materials_have_ranks(self):
        """All 10 materials should have unique ranks 1-10."""
        import pandas as pd
        from pathlib import Path

        data_path = Path(__file__).parent.parent / "data" / "processed" / "materials_master.csv"
        if data_path.exists():
            df = pd.read_csv(data_path)
            ranks = sorted(df["rank"].tolist())
            assert ranks == [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
