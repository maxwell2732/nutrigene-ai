"""Gene-nutrient interaction knowledge base.

Loads structured knowledge from YAML configs covering 10 gene-nutrient pairs
for Chinese population nutrigenomics: MTHFR, FTO, MC4R, APOE, FADS1/2,
TCF7L2, BCMO1, ADIPOQ, FGF21, VDR.
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional

from pydantic import ValidationError

from src.utils.config_loader import load_yaml_config
from src.utils.exceptions import ConfigValidationError, KnowledgeBaseError

from .data_models import EffectSize, GeneNutrientPair

logger = logging.getLogger(__name__)


class GeneNutrientKnowledgeBase:
    """Load, validate, and query the gene-nutrient knowledge base.

    Args:
        config_dir: Path to configs/gene_nutrient_kb/ directory.

    Raises:
        KnowledgeBaseError: If configs are missing or invalid.
    """

    def __init__(self, config_dir: Path) -> None:
        self.config_dir = config_dir
        self._pairs: Dict[str, GeneNutrientPair] = {}
        self._genes: Dict[str, dict] = {}
        self._allele_frequencies: Dict[str, dict] = {}
        self._recommendations: Dict[str, dict] = {}
        self._load()

    def _load(self) -> None:
        """Load all YAML configs and build validated GeneNutrientPair objects."""
        try:
            self._genes = load_yaml_config(self.config_dir / "genes.yaml")
            variants = load_yaml_config(self.config_dir / "variants.yaml")
            self._allele_frequencies = load_yaml_config(
                self.config_dir / "allele_frequencies.yaml"
            )
            effect_sizes = load_yaml_config(self.config_dir / "effect_sizes.yaml")
            self._recommendations = load_yaml_config(
                self.config_dir / "recommendations.yaml"
            )
        except Exception as e:
            raise KnowledgeBaseError(f"Failed to load knowledge base: {e}") from e

        for variant_id, vdata in variants.items():
            self._build_pair(variant_id, vdata, effect_sizes)

        logger.info(
            "Loaded %d gene-nutrient pairs from %s",
            len(self._pairs),
            self.config_dir,
        )

    def _build_pair(
        self, variant_id: str, vdata: dict, effect_sizes: dict
    ) -> None:
        """Build and store a single GeneNutrientPair from config data."""
        if variant_id not in effect_sizes:
            raise ConfigValidationError(
                f"Missing effect size for variant {variant_id}"
            )
        if variant_id not in self._allele_frequencies:
            raise ConfigValidationError(
                f"Missing allele frequency for variant {variant_id}"
            )

        try:
            pair = GeneNutrientPair(
                gene=vdata["gene"],
                variant_rsid=vdata["rsid"],
                nutrient=vdata["nutrient"],
                risk_allele=vdata["risk_allele"],
                protective_allele=vdata["protective_allele"],
                effect_size=EffectSize(**effect_sizes[variant_id]),
                allele_freq_east_asian=self._allele_frequencies[variant_id][
                    "east_asian"
                ],
                evidence_level=vdata["evidence_level"],
                pubmed_ids=vdata.get("pubmed_ids", []),
            )
            self._pairs[variant_id] = pair
        except (KeyError, ValidationError) as e:
            raise ConfigValidationError(
                f"Variant {variant_id} validation failed: {e}"
            ) from e

    # -- Query methods --

    def get_pair_by_rsid(self, rsid: str) -> Optional[GeneNutrientPair]:
        """Retrieve gene-nutrient pair by rsID."""
        for pair in self._pairs.values():
            if pair.variant_rsid == rsid:
                return pair
        return None

    def get_pairs_by_gene(self, gene: str) -> List[GeneNutrientPair]:
        """Retrieve all variant pairs for a specific gene symbol."""
        return [p for p in self._pairs.values() if p.gene == gene]

    def get_all_tracked_rsids(self) -> List[str]:
        """Return all rsIDs tracked in the knowledge base."""
        return [p.variant_rsid for p in self._pairs.values()]

    def get_all_variant_ids(self) -> List[str]:
        """Return all internal variant identifiers (e.g., 'MTHFR_C677T')."""
        return list(self._pairs.keys())

    def get_gene_info(self, gene: str) -> Optional[dict]:
        """Return gene metadata from genes.yaml."""
        return self._genes.get(gene)

    def get_recommendation_rules(self, gene_key: str) -> Optional[dict]:
        """Return recommendation rules for a gene key (e.g., 'MTHFR')."""
        return self._recommendations.get(gene_key)

    def get_allele_freq(
        self, variant_id: str, population: str = "east_asian"
    ) -> Optional[float]:
        """Return allele frequency for a variant in a given population."""
        freq_data = self._allele_frequencies.get(variant_id)
        if freq_data is None:
            return None
        return freq_data.get(population)

    @property
    def pair_count(self) -> int:
        """Number of gene-nutrient pairs loaded."""
        return len(self._pairs)

    @property
    def gene_count(self) -> int:
        """Number of unique genes loaded."""
        return len(self._genes)
