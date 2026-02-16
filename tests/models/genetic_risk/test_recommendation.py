"""Tests for dietary recommendation engine."""

from pathlib import Path

import pytest

from src.models.genetic_risk.data_models import GeneticProfile, GeneticRiskReport
from src.models.genetic_risk.knowledge_base import GeneNutrientKnowledgeBase
from src.models.genetic_risk.recommendation import RecommendationEngine, _age_to_group
from src.models.genetic_risk.risk_scoring import RiskScoringEngine
from src.utils.exceptions import RecommendationError

CONFIGS_DIR = Path(__file__).parent.parent.parent.parent / "configs"


@pytest.fixture
def recommender(
    kb: GeneNutrientKnowledgeBase, scorer: RiskScoringEngine
) -> RecommendationEngine:
    """Create a recommendation engine."""
    return RecommendationEngine(kb, scorer, CONFIGS_DIR / "chinese_dri.yaml")


class TestReportGeneration:
    """Tests for full report generation."""

    def test_high_risk_report(
        self, recommender: RecommendationEngine, high_risk_profile: GeneticProfile
    ) -> None:
        report = recommender.generate_report(high_risk_profile, age=35, sex="female")
        assert isinstance(report, GeneticRiskReport)
        assert report.individual_id == "TEST_HIGH_001"
        assert len(report.risk_scores) > 0
        assert len(report.recommendations) > 0
        assert "注册营养师" in report.disclaimer

    def test_low_risk_report(
        self, recommender: RecommendationEngine, low_risk_profile: GeneticProfile
    ) -> None:
        report = recommender.generate_report(low_risk_profile, age=40, sex="male")
        assert len(report.risk_scores) > 0
        # Low risk should still have recommendations (at low priority)
        assert len(report.recommendations) > 0

    def test_partial_profile_report(
        self, recommender: RecommendationEngine, partial_profile: GeneticProfile
    ) -> None:
        report = recommender.generate_report(partial_profile, age=25, sex="female")
        assert len(report.missing_variants) > 0  # Many variants missing
        assert len(report.risk_scores) >= 1  # At least MTHFR

    def test_report_has_missing_variants(
        self, recommender: RecommendationEngine, partial_profile: GeneticProfile
    ) -> None:
        report = recommender.generate_report(partial_profile, age=30, sex="male")
        # Partial profile should report many missing rsIDs
        assert len(report.missing_variants) > 5


class TestRecommendationContent:
    """Tests for recommendation content quality."""

    def test_high_risk_folate_recommendation(
        self, recommender: RecommendationEngine, high_risk_profile: GeneticProfile
    ) -> None:
        report = recommender.generate_report(
            high_risk_profile, age=30, sex="female", traits=["folate_metabolism"]
        )
        folate_recs = [r for r in report.recommendations if r.nutrient == "folate"]
        assert len(folate_recs) == 1
        rec = folate_recs[0]
        assert rec.recommended_intake > rec.current_dri  # Should be increased
        assert rec.priority in ("high", "critical")
        assert len(rec.food_sources) > 0

    def test_recommendations_include_chinese_foods(
        self, recommender: RecommendationEngine, high_risk_profile: GeneticProfile
    ) -> None:
        report = recommender.generate_report(high_risk_profile, age=30, sex="male")
        all_foods = []
        for rec in report.recommendations:
            all_foods.extend(rec.food_sources)
        # Check for Chinese characters in food sources
        has_chinese = any("\u4e00" <= c <= "\u9fff" for food in all_foods for c in food)
        assert has_chinese, "Recommendations should include Chinese food names"

    def test_recommendations_sorted_by_priority(
        self, recommender: RecommendationEngine, high_risk_profile: GeneticProfile
    ) -> None:
        report = recommender.generate_report(high_risk_profile, age=30, sex="male")
        if len(report.recommendations) >= 2:
            priority_map = {"critical": 4, "high": 3, "medium": 2, "low": 1}
            priorities = [
                priority_map.get(r.priority, 0) for r in report.recommendations
            ]
            assert priorities == sorted(priorities, reverse=True)

    def test_dri_varies_by_sex(
        self, recommender: RecommendationEngine, high_risk_profile: GeneticProfile
    ) -> None:
        report_f = recommender.generate_report(
            high_risk_profile, age=30, sex="female", traits=["folate_metabolism"]
        )
        report_m = recommender.generate_report(
            high_risk_profile, age=30, sex="male", traits=["folate_metabolism"]
        )
        # Folate DRI is same for both sexes (400), but energy differs
        # Check that engine doesn't crash for either sex
        assert len(report_f.recommendations) > 0
        assert len(report_m.recommendations) > 0


class TestInputValidation:
    """Tests for input validation in recommendation engine."""

    def test_invalid_sex_raises(
        self, recommender: RecommendationEngine, high_risk_profile: GeneticProfile
    ) -> None:
        with pytest.raises(RecommendationError, match="Invalid sex"):
            recommender.generate_report(high_risk_profile, age=30, sex="other")

    def test_invalid_age_raises(
        self, recommender: RecommendationEngine, high_risk_profile: GeneticProfile
    ) -> None:
        with pytest.raises(RecommendationError, match="Invalid age"):
            recommender.generate_report(high_risk_profile, age=-1, sex="male")


class TestAgeGroupMapping:
    """Tests for DRI age group mapping."""

    def test_young_adult(self) -> None:
        assert _age_to_group(25) == "18_49"

    def test_middle_age(self) -> None:
        assert _age_to_group(55) == "50_64"

    def test_elderly(self) -> None:
        assert _age_to_group(70) == "65_plus"

    def test_boundary_50(self) -> None:
        assert _age_to_group(50) == "50_64"

    def test_boundary_65(self) -> None:
        assert _age_to_group(65) == "65_plus"


class TestReportSerialization:
    """Tests for report JSON serialization."""

    def test_report_to_json(
        self, recommender: RecommendationEngine, high_risk_profile: GeneticProfile
    ) -> None:
        report = recommender.generate_report(high_risk_profile, age=30, sex="male")
        json_str = report.model_dump_json(indent=2)
        assert "individual_id" in json_str
        assert "TEST_HIGH_001" in json_str
        assert "recommendations" in json_str

    def test_report_summary(
        self, recommender: RecommendationEngine, high_risk_profile: GeneticProfile
    ) -> None:
        report = recommender.generate_report(high_risk_profile, age=30, sex="male")
        summary = report.to_summary()
        assert "individual_id" in summary
        assert summary["n_risk_scores"] > 0
