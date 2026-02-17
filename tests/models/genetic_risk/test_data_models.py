"""Tests for Pydantic data models."""

import pytest
from pydantic import ValidationError

from src.models.genetic_risk.data_models import (
    DietaryRecommendation,
    EffectSize,
    GeneticProfile,
    GeneticRiskReport,
    RiskScore,
    SNPGenotype,
    Zygosity,
)


class TestSNPGenotype:
    """Tests for SNPGenotype model."""

    def test_valid_genotype(self) -> None:
        g = SNPGenotype(
            rsid="rs1801133",
            chromosome="1",
            position=11856378,
            reference_allele="C",
            alternate_allele="T",
            genotype="CT",
            zygosity=Zygosity.HETEROZYGOUS,
        )
        assert g.rsid == "rs1801133"
        assert g.quality_score is None

    def test_invalid_rsid_rejected(self) -> None:
        with pytest.raises(ValidationError):
            SNPGenotype(
                rsid="invalid",
                chromosome="1",
                position=100,
                reference_allele="C",
                alternate_allele="T",
                genotype="CT",
                zygosity=Zygosity.HETEROZYGOUS,
            )

    def test_invalid_genotype_pattern_rejected(self) -> None:
        with pytest.raises(ValidationError):
            SNPGenotype(
                rsid="rs123",
                chromosome="1",
                position=100,
                reference_allele="C",
                alternate_allele="T",
                genotype="XY",
                zygosity=Zygosity.HETEROZYGOUS,
            )

    def test_quality_score_bounds(self) -> None:
        with pytest.raises(ValidationError):
            SNPGenotype(
                rsid="rs123",
                chromosome="1",
                position=100,
                reference_allele="C",
                alternate_allele="T",
                genotype="CT",
                zygosity=Zygosity.HETEROZYGOUS,
                quality_score=101.0,
            )

    def test_position_must_be_positive(self) -> None:
        with pytest.raises(ValidationError):
            SNPGenotype(
                rsid="rs123",
                chromosome="1",
                position=0,
                reference_allele="C",
                alternate_allele="T",
                genotype="CT",
                zygosity=Zygosity.HETEROZYGOUS,
            )


class TestGeneticProfile:
    """Tests for GeneticProfile model."""

    def test_valid_profile(self, high_risk_profile: GeneticProfile) -> None:
        assert high_risk_profile.individual_id == "TEST_HIGH_001"
        assert high_risk_profile.population == "han_chinese"
        assert len(high_risk_profile.genotypes) > 0

    def test_get_genotype_by_rsid(self, high_risk_profile: GeneticProfile) -> None:
        g = high_risk_profile.get_genotype_by_rsid("rs1801133")
        assert g is not None
        assert g.genotype == "TT"

    def test_get_missing_rsid_returns_none(
        self, high_risk_profile: GeneticProfile
    ) -> None:
        assert high_risk_profile.get_genotype_by_rsid("rs999999") is None

    def test_get_available_rsids(self, high_risk_profile: GeneticProfile) -> None:
        rsids = high_risk_profile.get_available_rsids()
        assert "rs1801133" in rsids
        assert "rs9939609" in rsids

    def test_empty_genotypes_rejected(self) -> None:
        with pytest.raises(ValidationError):
            GeneticProfile(
                individual_id="empty",
                genotypes=[],
                data_source="test",
            )


class TestEffectSize:
    """Tests for EffectSize model."""

    def test_valid_effect_size(self) -> None:
        es = EffectSize(value=0.39, ci_lower=0.31, ci_upper=0.47, unit="kg/m²")
        assert es.value == 0.39
        assert es.population == "east_asian"

    def test_ci_upper_must_be_gte_lower(self) -> None:
        with pytest.raises(ValidationError, match="ci_upper"):
            EffectSize(value=0.5, ci_lower=0.6, ci_upper=0.4, unit="kg/m²")


class TestRiskScore:
    """Tests for RiskScore model."""

    def test_valid_risk_score(self) -> None:
        rs = RiskScore(
            trait="obesity",
            score=1.5,
            percentile=93.3,
            risk_category="high",
            contributing_variants=["rs9939609", "rs17782313"],
        )
        assert rs.trait == "obesity"
        assert rs.risk_category == "high"

    def test_percentile_bounds(self) -> None:
        with pytest.raises(ValidationError):
            RiskScore(
                trait="test",
                score=0,
                percentile=101,
                contributing_variants=["rs1"],
            )


class TestGeneticRiskReport:
    """Tests for GeneticRiskReport model."""

    def test_default_report(self) -> None:
        report = GeneticRiskReport(individual_id="TEST_001")
        assert report.individual_id == "TEST_001"
        assert len(report.limitations) > 0
        assert "注册营养师" in report.disclaimer

    def test_summary(self) -> None:
        report = GeneticRiskReport(
            individual_id="TEST_001",
            recommendations=[
                DietaryRecommendation(
                    nutrient="folate",
                    current_dri=400,
                    recommended_intake=700,
                    unit="μg/day",
                    adjustment_reason="MTHFR TT",
                    priority="high",
                ),
            ],
        )
        summary = report.to_summary()
        assert summary["n_recommendations"] == 1
        assert "folate" in summary["high_priority"]
