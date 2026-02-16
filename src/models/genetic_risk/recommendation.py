"""Dietary recommendation engine based on genetic risk.

Generates personalized dietary recommendations using Chinese Dietary
Reference Intakes (2022) as baseline, adjusted by individual genetic
risk profiles.
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from src.utils.config_loader import load_yaml_config
from src.utils.exceptions import RecommendationError

from .data_models import DietaryRecommendation, GeneticProfile, GeneticRiskReport, RiskScore
from .knowledge_base import GeneNutrientKnowledgeBase
from .risk_scoring import RiskScoringEngine, TRAIT_GENE_KEY, TRAIT_VARIANT_MAP
from .validators import GeneticDataValidator

logger = logging.getLogger(__name__)

# Priority sort order
_PRIORITY_ORDER = {"critical": 4, "high": 3, "medium": 2, "low": 1}


class RecommendationEngine:
    """Generate personalized dietary recommendations from genetic risk.

    Rule-based v1 implementation using genotype-specific recommendation
    rules from YAML config, with Chinese DRIs as baseline.

    Args:
        knowledge_base: Loaded GeneNutrientKnowledgeBase.
        scoring_engine: Initialized RiskScoringEngine.
        dri_config_path: Path to configs/chinese_dri.yaml.
    """

    def __init__(
        self,
        knowledge_base: GeneNutrientKnowledgeBase,
        scoring_engine: RiskScoringEngine,
        dri_config_path: Path,
    ) -> None:
        self.kb = knowledge_base
        self.scorer = scoring_engine
        self.dri = load_yaml_config(dri_config_path)

    def generate_report(
        self,
        profile: GeneticProfile,
        age: int,
        sex: str,
        traits: Optional[List[str]] = None,
    ) -> GeneticRiskReport:
        """Generate a complete genetic risk report with recommendations.

        Args:
            profile: Individual genetic profile.
            age: Age in years.
            sex: 'male' or 'female'.
            traits: Optional subset of traits to assess; defaults to all.

        Returns:
            Complete GeneticRiskReport.
        """
        if sex not in ("male", "female"):
            raise RecommendationError(f"Invalid sex: {sex}. Must be 'male' or 'female'.")
        if age < 0 or age > 150:
            raise RecommendationError(f"Invalid age: {age}")

        # Determine which traits to score
        target_traits = traits if traits else list(TRAIT_VARIANT_MAP.keys())

        # Calculate risk scores
        risk_scores: List[RiskScore] = []
        for trait in target_traits:
            rsids = TRAIT_VARIANT_MAP.get(trait, [])
            result = self.scorer.calculate_polygenic_risk(profile, trait, rsids)
            if result is not None:
                risk_scores.append(result)

        # Find missing variants
        all_required = self.kb.get_all_tracked_rsids()
        missing = GeneticDataValidator.get_missing_rsids(profile, all_required)

        # Generate recommendations
        recommendations = self._build_recommendations(risk_scores, age, sex)

        # Sort by priority
        recommendations.sort(
            key=lambda r: _PRIORITY_ORDER.get(r.priority, 0), reverse=True
        )

        return GeneticRiskReport(
            individual_id=profile.individual_id,
            generated_date=datetime.now().isoformat(),
            population=profile.population,
            risk_scores=risk_scores,
            recommendations=recommendations,
            missing_variants=missing,
        )

    def _build_recommendations(
        self, risk_scores: List[RiskScore], age: int, sex: str
    ) -> List[DietaryRecommendation]:
        """Build dietary recommendations from risk scores.

        Args:
            risk_scores: List of calculated RiskScore objects.
            age: Age in years.
            sex: 'male' or 'female'.

        Returns:
            List of DietaryRecommendation objects.
        """
        recommendations: List[DietaryRecommendation] = []

        for score in risk_scores:
            gene_key = TRAIT_GENE_KEY.get(score.trait)
            if gene_key is None:
                logger.warning("No gene key mapping for trait %s", score.trait)
                continue

            rules = self.kb.get_recommendation_rules(gene_key)
            if rules is None:
                logger.warning("No recommendation rules for gene %s", gene_key)
                continue

            rec = self._apply_rules(rules, score, age, sex)
            if rec is not None:
                recommendations.append(rec)

        return recommendations

    def _apply_rules(
        self, rules: dict, score: RiskScore, age: int, sex: str
    ) -> Optional[DietaryRecommendation]:
        """Apply genotype-specific rules to produce a recommendation.

        Args:
            rules: Recommendation rules from YAML config.
            score: RiskScore for the relevant trait.
            age: Age in years.
            sex: 'male' or 'female'.

        Returns:
            DietaryRecommendation or None if rules incomplete.
        """
        # Select rule tier based on risk category
        tier_key = f"{score.risk_category}_risk"
        tier = rules.get(tier_key)
        if tier is None:
            logger.warning("No %s tier in rules for trait %s", tier_key, score.trait)
            return None

        nutrient = rules.get("nutrient", score.trait)
        base_dri = self._get_dri(nutrient, age, sex)

        if base_dri is None:
            logger.warning("No DRI found for nutrient %s (age=%d, sex=%s)", nutrient, age, sex)
            return None

        multiplier = tier.get("dri_multiplier", 1.0)
        recommended = round(base_dri * multiplier, 1)

        # Build the reason string
        description = tier.get("description", "")
        supplementation = tier.get("supplementation", "")
        reason = description
        if supplementation and supplementation != "Not applicable":
            reason = f"{description} {supplementation}"

        return DietaryRecommendation(
            nutrient=nutrient,
            current_dri=base_dri,
            recommended_intake=recommended,
            unit=self._get_dri_unit(nutrient),
            adjustment_reason=reason,
            food_sources=tier.get("food_sources", []),
            priority=tier.get("priority", "medium"),
            evidence_level=self._get_evidence_level(score),
        )

    def _get_dri(self, nutrient: str, age: int, sex: str) -> Optional[float]:
        """Look up Chinese DRI for a nutrient by age and sex.

        Args:
            nutrient: Nutrient key from chinese_dri.yaml.
            age: Age in years.
            sex: 'male' or 'female'.

        Returns:
            DRI value or None if not found.
        """
        # Map recommendation nutrient names to DRI config keys
        nutrient_map = {
            "folate": "folate",
            "energy_balance": "energy",
            "dietary_fat": "dietary_fat",
            "omega3_omega6": "omega3_epa_dha",
            "carbohydrate": "carbohydrate",
            "vitamin_a": "vitamin_a",
            "insulin_sensitivity": "protein",  # proxy: general metabolic
            "macronutrient_preference": "carbohydrate",
            "vitamin_d_calcium": "vitamin_d",
        }

        dri_key = nutrient_map.get(nutrient, nutrient)
        nutrient_data = self.dri.get(dri_key)
        if nutrient_data is None:
            return None

        age_group = _age_to_group(age)
        lookup_key = f"adult_{sex}_{age_group}"
        value = nutrient_data.get(lookup_key)

        if value is None:
            # Fallback: try without age group
            fallback_key = f"adult_{sex}_18_49"
            value = nutrient_data.get(fallback_key)

        return value

    def _get_dri_unit(self, nutrient: str) -> str:
        """Get unit string for a nutrient from DRI config."""
        nutrient_map = {
            "folate": "folate",
            "energy_balance": "energy",
            "dietary_fat": "dietary_fat",
            "omega3_omega6": "omega3_epa_dha",
            "carbohydrate": "carbohydrate",
            "vitamin_a": "vitamin_a",
            "insulin_sensitivity": "protein",
            "macronutrient_preference": "carbohydrate",
            "vitamin_d_calcium": "vitamin_d",
        }
        dri_key = nutrient_map.get(nutrient, nutrient)
        nutrient_data = self.dri.get(dri_key)
        if nutrient_data is None:
            return "units"
        return nutrient_data.get("unit", "units")

    @staticmethod
    def _get_evidence_level(score: RiskScore) -> str:
        """Derive evidence level from confidence."""
        mapping = {"high": "A", "medium": "B", "low": "C"}
        return mapping.get(score.confidence, "B")


def _age_to_group(age: int) -> str:
    """Convert age to Chinese DRI age group string.

    Age groups per Chinese DRI 2022:
        18-49, 50-64, 65+
    """
    if age < 50:
        return "18_49"
    elif age < 65:
        return "50_64"
    else:
        return "65_plus"
