"""Tests for genetic risk scoring engine."""

import pytest

from src.models.genetic_risk.data_models import GeneticProfile
from src.models.genetic_risk.risk_scoring import (
    RiskScoringEngine,
    _categorize_risk,
    _z_to_percentile,
)
from src.utils.exceptions import RiskScoringError


class TestSingleGeneScoring:
    """Tests for single-gene risk score calculation."""

    def test_mthfr_tt_is_high_risk(
        self, scorer: RiskScoringEngine, high_risk_profile: GeneticProfile
    ) -> None:
        score = scorer.calculate_single_gene_risk(high_risk_profile, "rs1801133")
        assert score is not None
        assert score.risk_category == "high"
        assert score.score > 0
        assert score.confidence == "high"  # Evidence level A

    def test_mthfr_cc_is_low_risk(
        self, scorer: RiskScoringEngine, low_risk_profile: GeneticProfile
    ) -> None:
        score = scorer.calculate_single_gene_risk(low_risk_profile, "rs1801133")
        assert score is not None
        assert score.risk_category == "low"
        assert score.score < 0

    def test_mthfr_ct_is_moderate(
        self, scorer: RiskScoringEngine, moderate_risk_profile: GeneticProfile
    ) -> None:
        score = scorer.calculate_single_gene_risk(moderate_risk_profile, "rs1801133")
        assert score is not None
        assert score.risk_category == "moderate"

    def test_missing_rsid_returns_none(
        self, scorer: RiskScoringEngine, low_risk_profile: GeneticProfile
    ) -> None:
        result = scorer.calculate_single_gene_risk(low_risk_profile, "rs838133")
        assert result is None

    def test_unknown_rsid_raises(
        self, scorer: RiskScoringEngine, high_risk_profile: GeneticProfile
    ) -> None:
        # Inject a fake genotype into the profile to test KB miss
        from src.models.genetic_risk.data_models import SNPGenotype, Zygosity

        fake = SNPGenotype(
            rsid="rs999999",
            chromosome="1",
            position=1,
            reference_allele="A",
            alternate_allele="G",
            genotype="AG",
            zygosity=Zygosity.HETEROZYGOUS,
        )
        high_risk_profile.genotypes.append(fake)
        with pytest.raises(RiskScoringError):
            scorer.calculate_single_gene_risk(high_risk_profile, "rs999999")

    def test_score_has_percentile(
        self, scorer: RiskScoringEngine, high_risk_profile: GeneticProfile
    ) -> None:
        score = scorer.calculate_single_gene_risk(high_risk_profile, "rs9939609")
        assert score is not None
        assert 0 <= score.percentile <= 100

    def test_contributing_variants_listed(
        self, scorer: RiskScoringEngine, high_risk_profile: GeneticProfile
    ) -> None:
        score = scorer.calculate_single_gene_risk(high_risk_profile, "rs1801133")
        assert score is not None
        assert "rs1801133" in score.contributing_variants


class TestPolygenicScoring:
    """Tests for polygenic risk score calculation."""

    def test_obesity_polygenic_high_risk(
        self, scorer: RiskScoringEngine, high_risk_profile: GeneticProfile
    ) -> None:
        score = scorer.calculate_polygenic_risk(
            high_risk_profile, "obesity", ["rs9939609", "rs17782313", "rs12970134"]
        )
        assert score is not None
        assert score.trait == "obesity"
        assert score.risk_category == "high"
        assert len(score.contributing_variants) == 3

    def test_polygenic_low_risk(
        self, scorer: RiskScoringEngine, low_risk_profile: GeneticProfile
    ) -> None:
        score = scorer.calculate_polygenic_risk(
            low_risk_profile, "obesity", ["rs9939609"]
        )
        assert score is not None
        assert score.risk_category == "low"

    def test_polygenic_with_missing_variants(
        self, scorer: RiskScoringEngine, partial_profile: GeneticProfile
    ) -> None:
        # partial_profile only has rs1801133
        score = scorer.calculate_polygenic_risk(
            partial_profile,
            "folate_metabolism",
            ["rs1801133", "rs1801131"],
        )
        assert score is not None
        assert len(score.contributing_variants) == 1

    def test_polygenic_all_missing_returns_none(
        self, scorer: RiskScoringEngine, partial_profile: GeneticProfile
    ) -> None:
        result = scorer.calculate_polygenic_risk(
            partial_profile, "obesity", ["rs9939609", "rs17782313"]
        )
        assert result is None


class TestAPOEScoring:
    """Tests for APOE epsilon genotype determination."""

    def test_apoe_e4_e4_high_risk(
        self, scorer: RiskScoringEngine, high_risk_profile: GeneticProfile
    ) -> None:
        score = scorer.calculate_polygenic_risk(
            high_risk_profile, "lipid_metabolism", ["rs429358", "rs7412"]
        )
        assert score is not None
        assert score.risk_category == "high"
        assert "rs429358" in score.contributing_variants

    def test_apoe_e3_e4_moderate(
        self, scorer: RiskScoringEngine, moderate_risk_profile: GeneticProfile
    ) -> None:
        score = scorer.calculate_polygenic_risk(
            moderate_risk_profile, "lipid_metabolism", ["rs429358", "rs7412"]
        )
        assert score is not None
        assert score.risk_category == "moderate"

    def test_apoe_e3_e3_low(
        self, scorer: RiskScoringEngine, low_risk_profile: GeneticProfile
    ) -> None:
        score = scorer.calculate_polygenic_risk(
            low_risk_profile, "lipid_metabolism", ["rs429358", "rs7412"]
        )
        assert score is not None
        assert score.risk_category == "low"


class TestScoreAllTraits:
    """Tests for scoring all traits at once."""

    def test_score_all_returns_multiple(
        self, scorer: RiskScoringEngine, high_risk_profile: GeneticProfile
    ) -> None:
        results = scorer.score_all_traits(high_risk_profile)
        assert len(results) >= 5  # Many traits have data in high_risk profile
        traits = {r.trait for r in results}
        assert "obesity" in traits
        assert "folate_metabolism" in traits

    def test_partial_profile_scores_available(
        self, scorer: RiskScoringEngine, partial_profile: GeneticProfile
    ) -> None:
        results = scorer.score_all_traits(partial_profile)
        assert len(results) >= 1
        traits = {r.trait for r in results}
        assert "folate_metabolism" in traits


class TestHelpers:
    """Tests for helper functions."""

    def test_z_to_percentile_zero(self) -> None:
        assert abs(_z_to_percentile(0) - 50.0) < 0.1

    def test_z_to_percentile_high(self) -> None:
        assert _z_to_percentile(2.0) > 95

    def test_z_to_percentile_low(self) -> None:
        assert _z_to_percentile(-2.0) < 5

    def test_categorize_risk(self) -> None:
        assert _categorize_risk(-1.0) == "low"
        assert _categorize_risk(0.0) == "moderate"
        assert _categorize_risk(1.0) == "high"
