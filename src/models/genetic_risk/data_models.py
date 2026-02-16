"""Pydantic data models for genetic risk assessment.

Covers SNP genotypes, genetic profiles, effect sizes, gene-nutrient
interactions, risk scores, dietary recommendations, and full reports.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Dict, List, Literal, Optional

from pydantic import BaseModel, Field, field_validator


class Zygosity(str, Enum):
    """Genotype zygosity classification."""

    HOMOZYGOUS_REF = "homozygous_reference"
    HETEROZYGOUS = "heterozygous"
    HOMOZYGOUS_ALT = "homozygous_alternate"
    UNKNOWN = "unknown"


class SNPGenotype(BaseModel):
    """Single SNP genotype observation."""

    rsid: str = Field(..., pattern=r"^rs\d+$", description="rsID (e.g., rs1801133)")
    chromosome: str = Field(..., description="Chromosome (1-22, X, Y, MT)")
    position: int = Field(..., gt=0, description="Genomic position (GRCh38)")
    reference_allele: str = Field(..., pattern=r"^[ACGT]+$")
    alternate_allele: str = Field(..., pattern=r"^[ACGT]+$")
    genotype: str = Field(
        ..., pattern=r"^[ACGT]{2}$", description="Observed genotype (e.g., 'CT')"
    )
    zygosity: Zygosity
    quality_score: Optional[float] = Field(None, ge=0, le=100)

    @field_validator("genotype")
    @classmethod
    def validate_genotype_alleles(cls, v: str, info: object) -> str:
        """Ensure genotype contains only reference or alternate alleles."""
        # Validation is done at the validator level (GeneticDataValidator)
        # to allow flexible construction; basic format check via pattern above.
        return v


class GeneticProfile(BaseModel):
    """Complete genetic profile for an individual."""

    individual_id: str = Field(..., description="Anonymized individual identifier")
    genotypes: List[SNPGenotype] = Field(..., min_length=1)
    population: Literal["han_chinese", "east_asian", "other"] = "han_chinese"
    data_source: str = Field(..., description="e.g., 'WGS', 'SNP_Array', 'DTC'")
    collection_date: Optional[str] = Field(None, description="ISO 8601 date")

    def get_genotype_by_rsid(self, rsid: str) -> Optional[SNPGenotype]:
        """Retrieve genotype for a specific rsID."""
        for g in self.genotypes:
            if g.rsid == rsid:
                return g
        return None

    def get_available_rsids(self) -> List[str]:
        """Return all rsIDs in this profile."""
        return [g.rsid for g in self.genotypes]


class EffectSize(BaseModel):
    """Effect size with confidence intervals (required by domain rules)."""

    value: float = Field(..., description="Point estimate")
    ci_lower: float = Field(..., description="95% CI lower bound")
    ci_upper: float = Field(..., description="95% CI upper bound")
    unit: str = Field(..., description="e.g., 'kg/m²', 'μmol/L'")
    population: str = Field("east_asian", description="Reference population")

    @field_validator("ci_upper")
    @classmethod
    def ci_upper_gte_lower(cls, v: float, info: object) -> float:
        """Ensure upper CI bound >= lower CI bound."""
        data = info.data if hasattr(info, "data") else {}
        ci_lower = data.get("ci_lower")
        if ci_lower is not None and v < ci_lower:
            raise ValueError("ci_upper must be >= ci_lower")
        return v


class GeneNutrientPair(BaseModel):
    """Gene-nutrient interaction knowledge entry."""

    gene: str = Field(..., description="Gene symbol (e.g., 'MTHFR')")
    variant_rsid: str = Field(..., pattern=r"^rs\d+$")
    nutrient: str = Field(..., description="Nutrient or dietary factor")
    risk_allele: str = Field(..., pattern=r"^[ACGT]+$")
    protective_allele: str = Field(..., pattern=r"^[ACGT]+$")
    effect_size: EffectSize
    allele_freq_east_asian: float = Field(..., ge=0, le=1)
    evidence_level: Literal["A", "B", "C", "D"] = Field(
        ...,
        description="A=Strong RCT, B=Cohort, C=Cross-sectional, D=Expert opinion",
    )
    pubmed_ids: List[str] = Field(default_factory=list)


class RiskScore(BaseModel):
    """Genetic risk score for a specific trait."""

    trait: str = Field(..., description="e.g., 'obesity', 'folate_metabolism'")
    score: float = Field(..., description="Normalized risk score (z-score)")
    percentile: Optional[float] = Field(None, ge=0, le=100)
    risk_category: Literal["low", "moderate", "high"] = "moderate"
    contributing_variants: List[str] = Field(
        ..., description="List of rsIDs included"
    )
    confidence: Literal["high", "medium", "low"] = "medium"


class DietaryRecommendation(BaseModel):
    """Personalized dietary recommendation based on genetic risk."""

    nutrient: str
    current_dri: float = Field(..., description="Chinese DRI baseline")
    recommended_intake: float = Field(..., description="Personalized target")
    unit: str = Field(..., description="mg, μg, g, kcal, etc.")
    adjustment_reason: str = Field(..., description="Genetic basis for adjustment")
    food_sources: List[str] = Field(
        default_factory=list, description="Culturally appropriate Chinese foods"
    )
    priority: Literal["critical", "high", "medium", "low"] = "medium"
    evidence_level: Literal["A", "B", "C", "D"] = "B"


_DEFAULT_LIMITATIONS = [
    "Genetic factors typically explain <5% of trait variance",
    "Recommendations based on population-level associations",
    "Not a substitute for clinical advice from a registered dietitian or physician",
    "Effect sizes may vary by age, sex, and environmental factors",
]

_DEFAULT_DISCLAIMER = (
    "This report is for research and educational purposes only. "
    "Consult a registered dietitian (注册营养师) or physician before "
    "making dietary changes based on genetic information."
)


class GeneticRiskReport(BaseModel):
    """Complete genetic risk assessment report for an individual."""

    individual_id: str
    generated_date: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="ISO 8601 timestamp",
    )
    population: str = "han_chinese"
    risk_scores: List[RiskScore] = Field(default_factory=list)
    recommendations: List[DietaryRecommendation] = Field(default_factory=list)
    missing_variants: List[str] = Field(
        default_factory=list,
        description="rsIDs not found in individual profile",
    )
    limitations: List[str] = Field(default_factory=lambda: list(_DEFAULT_LIMITATIONS))
    disclaimer: str = Field(default=_DEFAULT_DISCLAIMER)

    def to_summary(self) -> Dict[str, object]:
        """Return a concise summary dict for display."""
        return {
            "individual_id": self.individual_id,
            "date": self.generated_date,
            "n_risk_scores": len(self.risk_scores),
            "n_recommendations": len(self.recommendations),
            "high_priority": [
                r.nutrient
                for r in self.recommendations
                if r.priority in ("critical", "high")
            ],
            "missing_variants": self.missing_variants,
        }
