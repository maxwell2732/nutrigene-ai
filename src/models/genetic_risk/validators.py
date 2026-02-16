"""Genetic data validation utilities.

Validates genotype consistency, profile completeness, and data quality
for use in risk scoring pipelines.
"""

import logging
from typing import Dict, List

from src.utils.exceptions import GeneticDataValidationError

from .data_models import GeneticProfile, SNPGenotype

logger = logging.getLogger(__name__)


class GeneticDataValidator:
    """Validate genetic data quality and consistency."""

    @staticmethod
    def validate_genotype_consistency(genotype: SNPGenotype) -> bool:
        """Check that observed genotype matches reference/alternate alleles.

        Args:
            genotype: SNPGenotype to validate.

        Returns:
            True if valid.

        Raises:
            GeneticDataValidationError: If genotype is inconsistent.
        """
        ref = genotype.reference_allele
        alt = genotype.alternate_allele
        obs = genotype.genotype

        valid_genotypes = {ref + ref, ref + alt, alt + ref, alt + alt}

        if obs not in valid_genotypes:
            raise GeneticDataValidationError(
                f"Genotype '{obs}' inconsistent with ref={ref}, alt={alt} "
                f"for {genotype.rsid}"
            )
        return True

    @staticmethod
    def validate_profile_completeness(
        profile: GeneticProfile, required_rsids: List[str]
    ) -> Dict[str, bool]:
        """Check which required variants are present in a profile.

        Args:
            profile: GeneticProfile to check.
            required_rsids: List of required rsIDs.

        Returns:
            Dict mapping rsID to presence (True/False).
        """
        available = {g.rsid for g in profile.genotypes}
        return {rsid: rsid in available for rsid in required_rsids}

    @staticmethod
    def get_missing_rsids(
        profile: GeneticProfile, required_rsids: List[str]
    ) -> List[str]:
        """Return rsIDs that are required but missing from the profile.

        Args:
            profile: GeneticProfile to check.
            required_rsids: List of required rsIDs.

        Returns:
            List of missing rsIDs.
        """
        available = {g.rsid for g in profile.genotypes}
        return [rsid for rsid in required_rsids if rsid not in available]

    @staticmethod
    def flag_low_quality_genotypes(
        profile: GeneticProfile, min_quality: float = 20.0
    ) -> List[str]:
        """Identify genotypes below quality threshold.

        Args:
            profile: GeneticProfile to check.
            min_quality: Minimum acceptable quality score.

        Returns:
            List of low-quality rsIDs.
        """
        low_quality = []
        for genotype in profile.genotypes:
            if (
                genotype.quality_score is not None
                and genotype.quality_score < min_quality
            ):
                low_quality.append(genotype.rsid)
                logger.warning(
                    "Low quality genotype: %s (Q=%.1f)",
                    genotype.rsid,
                    genotype.quality_score,
                )
        return low_quality

    @staticmethod
    def validate_profile(
        profile: GeneticProfile, required_rsids: List[str]
    ) -> Dict[str, object]:
        """Run all validations on a profile and return a summary.

        Args:
            profile: GeneticProfile to validate.
            required_rsids: List of required rsIDs.

        Returns:
            Dict with keys: valid (bool), missing (list), low_quality (list),
            inconsistent (list).
        """
        missing = GeneticDataValidator.get_missing_rsids(profile, required_rsids)
        low_quality = GeneticDataValidator.flag_low_quality_genotypes(profile)

        inconsistent: List[str] = []
        for genotype in profile.genotypes:
            try:
                GeneticDataValidator.validate_genotype_consistency(genotype)
            except GeneticDataValidationError:
                inconsistent.append(genotype.rsid)

        is_valid = len(inconsistent) == 0 and len(profile.genotypes) > 0

        return {
            "valid": is_valid,
            "missing": missing,
            "low_quality": low_quality,
            "inconsistent": inconsistent,
            "total_variants": len(profile.genotypes),
            "coverage": (
                (len(required_rsids) - len(missing)) / len(required_rsids)
                if required_rsids
                else 0.0
            ),
        }
