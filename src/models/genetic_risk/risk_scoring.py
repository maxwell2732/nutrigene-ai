"""Genetic risk scoring engine.

Calculates single-gene and polygenic risk scores from genotype data,
normalized against East Asian population allele frequencies.
"""

import logging
import math
from typing import List, Optional

from src.utils.exceptions import RiskScoringError

from .data_models import GeneticProfile, RiskScore
from .knowledge_base import GeneNutrientKnowledgeBase

logger = logging.getLogger(__name__)

# APOE epsilon allele definitions (rs429358, rs7412)
# rs429358 T→C and rs7412 C→T define the three alleles:
#   e2: rs429358=T, rs7412=T
#   e3: rs429358=T, rs7412=C  (reference/most common)
#   e4: rs429358=C, rs7412=C
APOE_EPSILON_MAP = {
    ("TT", "TT"): "e2/e2",
    ("TT", "CT"): "e2/e3",
    ("TT", "CC"): "e3/e3",
    ("CT", "CC"): "e3/e4",
    ("CC", "CC"): "e4/e4",
    ("CT", "CT"): "e2/e4",
    # Reversed order handling
    ("TT", "TC"): "e2/e3",
    ("TC", "CC"): "e3/e4",
    ("TC", "TC"): "e2/e4",
}

# Risk levels for APOE epsilon genotypes (0=low, 1=moderate, 2=high)
APOE_RISK_LEVELS = {
    "e2/e2": 0,
    "e2/e3": 0,
    "e3/e3": 0,
    "e3/e4": 1,
    "e4/e4": 2,
    "e2/e4": 1,
}

# Trait-to-variant mappings for polygenic scoring
TRAIT_VARIANT_MAP = {
    "obesity": ["rs9939609", "rs17782313", "rs12970134"],
    "folate_metabolism": ["rs1801133", "rs1801131"],
    "fatty_acid_metabolism": ["rs174547", "rs498793"],
    "lipid_metabolism": ["rs429358", "rs7412"],
    "type2_diabetes": ["rs7903146"],
    "vitamin_a_conversion": ["rs12934922"],
    "metabolic_health": ["rs1501299"],
    "sweet_preference": ["rs838133"],
    "bone_health": ["rs2228570"],
}

# Map trait → gene key (for recommendation lookup)
TRAIT_GENE_KEY = {
    "obesity": "FTO",
    "folate_metabolism": "MTHFR",
    "fatty_acid_metabolism": "FADS",
    "lipid_metabolism": "APOE",
    "type2_diabetes": "TCF7L2",
    "vitamin_a_conversion": "BCMO1",
    "metabolic_health": "ADIPOQ",
    "sweet_preference": "FGF21",
    "bone_health": "VDR",
}


class RiskScoringEngine:
    """Calculate genetic risk scores for nutrition-related traits.

    Supports single-gene scoring, polygenic risk scoring, and
    APOE epsilon genotype determination.

    Args:
        knowledge_base: Loaded GeneNutrientKnowledgeBase instance.
    """

    def __init__(self, knowledge_base: GeneNutrientKnowledgeBase) -> None:
        self.kb = knowledge_base

    def calculate_single_gene_risk(
        self, profile: GeneticProfile, rsid: str
    ) -> Optional[RiskScore]:
        """Calculate risk score for a single SNP variant.

        Uses an additive model: score = effect_size * risk_allele_count,
        normalized to a z-score against the East Asian population.

        Args:
            profile: Individual genetic profile.
            rsid: SNP identifier (e.g., 'rs1801133').

        Returns:
            RiskScore or None if variant not in profile.

        Raises:
            RiskScoringError: If rsid not in knowledge base.
        """
        genotype = profile.get_genotype_by_rsid(rsid)
        if genotype is None:
            logger.warning(
                "rsID %s not found in profile %s", rsid, profile.individual_id
            )
            return None

        pair = self.kb.get_pair_by_rsid(rsid)
        if pair is None:
            raise RiskScoringError(f"rsID {rsid} not in knowledge base")

        risk_allele_count = genotype.genotype.count(pair.risk_allele)
        raw_score = pair.effect_size.value * risk_allele_count

        # Population-normalized z-score (additive model)
        p = pair.allele_freq_east_asian
        expected = 2 * p * pair.effect_size.value
        variance = 2 * p * (1 - p) * pair.effect_size.value ** 2
        std_dev = math.sqrt(variance) if variance > 0 else 1.0
        z_score = (raw_score - expected) / std_dev

        percentile = _z_to_percentile(z_score)
        risk_category = _categorize_risk(z_score)

        return RiskScore(
            trait=f"{pair.gene}_{pair.nutrient}",
            score=round(z_score, 4),
            percentile=percentile,
            risk_category=risk_category,
            contributing_variants=[rsid],
            confidence="high" if pair.evidence_level in ("A", "B") else "medium",
        )

    def calculate_polygenic_risk(
        self, profile: GeneticProfile, trait: str, rsids: List[str]
    ) -> Optional[RiskScore]:
        """Calculate combined polygenic risk score across multiple variants.

        Args:
            profile: Individual genetic profile.
            trait: Trait name (e.g., 'obesity').
            rsids: List of rsIDs to include.

        Returns:
            Combined RiskScore, or None if no valid variants found.
        """
        # Special handling for APOE
        if trait == "lipid_metabolism":
            return self._score_apoe(profile)

        scores: List[float] = []
        contributing: List[str] = []

        for rsid in rsids:
            result = self.calculate_single_gene_risk(profile, rsid)
            if result is not None:
                scores.append(result.score)
                contributing.append(rsid)

        if not scores:
            return None

        combined = sum(scores) / len(scores)
        percentile = _z_to_percentile(combined)
        risk_category = _categorize_risk(combined)

        return RiskScore(
            trait=trait,
            score=round(combined, 4),
            percentile=percentile,
            risk_category=risk_category,
            contributing_variants=contributing,
            confidence="high" if len(contributing) >= 2 else "medium",
        )

    def _score_apoe(self, profile: GeneticProfile) -> Optional[RiskScore]:
        """Determine APOE epsilon genotype and assign risk category.

        APOE is special: two SNPs (rs429358, rs7412) define three alleles
        (e2, e3, e4). Risk is determined by epsilon genotype, not individual
        allele counts.

        Args:
            profile: Individual genetic profile.

        Returns:
            RiskScore for lipid metabolism, or None if APOE SNPs missing.
        """
        gt_429358 = profile.get_genotype_by_rsid("rs429358")
        gt_7412 = profile.get_genotype_by_rsid("rs7412")

        if gt_429358 is None or gt_7412 is None:
            logger.warning(
                "APOE SNPs missing for profile %s", profile.individual_id
            )
            return None

        key = (gt_429358.genotype, gt_7412.genotype)
        epsilon = APOE_EPSILON_MAP.get(key)

        if epsilon is None:
            logger.warning("Unrecognized APOE genotype combination: %s", key)
            return None

        risk_level = APOE_RISK_LEVELS.get(epsilon, 1)
        risk_category = {0: "low", 1: "moderate", 2: "high"}[risk_level]

        # Convert to approximate z-score for consistency
        z_score = {0: -0.8, 1: 0.0, 2: 1.2}[risk_level]

        return RiskScore(
            trait="lipid_metabolism",
            score=z_score,
            percentile=_z_to_percentile(z_score),
            risk_category=risk_category,
            contributing_variants=["rs429358", "rs7412"],
            confidence="high",
        )

    def score_all_traits(
        self, profile: GeneticProfile
    ) -> List[RiskScore]:
        """Calculate risk scores for all available traits.

        Args:
            profile: Individual genetic profile.

        Returns:
            List of RiskScore objects for all traits with available data.
        """
        results: List[RiskScore] = []

        for trait, rsids in TRAIT_VARIANT_MAP.items():
            result = self.calculate_polygenic_risk(profile, trait, rsids)
            if result is not None:
                results.append(result)

        return results


def _z_to_percentile(z_score: float) -> float:
    """Convert z-score to percentile (0-100) using error function."""
    percentile = 50 * (1 + math.erf(z_score / math.sqrt(2)))
    return round(percentile, 2)


def _categorize_risk(z_score: float) -> str:
    """Categorize risk based on z-score thresholds."""
    if z_score < -0.5:
        return "low"
    elif z_score < 0.5:
        return "moderate"
    else:
        return "high"
