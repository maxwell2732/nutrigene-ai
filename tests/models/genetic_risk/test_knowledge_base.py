"""Tests for gene-nutrient knowledge base."""

from pathlib import Path

import pytest

from src.models.genetic_risk.knowledge_base import GeneNutrientKnowledgeBase
from src.utils.exceptions import KnowledgeBaseError


class TestKnowledgeBase:
    """Tests for GeneNutrientKnowledgeBase loading and queries."""

    def test_loads_successfully(self, kb: GeneNutrientKnowledgeBase) -> None:
        assert kb.pair_count > 0
        assert kb.gene_count >= 10

    def test_all_10_genes_present(self, kb: GeneNutrientKnowledgeBase) -> None:
        expected_genes = [
            "MTHFR", "FTO", "MC4R", "APOE", "FADS1", "FADS2",
            "TCF7L2", "BCMO1", "ADIPOQ", "FGF21", "VDR",
        ]
        for gene in expected_genes:
            info = kb.get_gene_info(gene)
            assert info is not None, f"Gene {gene} missing from knowledge base"

    def test_get_pair_by_rsid(self, kb: GeneNutrientKnowledgeBase) -> None:
        pair = kb.get_pair_by_rsid("rs1801133")
        assert pair is not None
        assert pair.gene == "MTHFR"
        assert pair.risk_allele == "T"
        assert pair.evidence_level == "A"
        assert 0 < pair.allele_freq_east_asian < 1

    def test_get_pair_by_rsid_not_found(
        self, kb: GeneNutrientKnowledgeBase
    ) -> None:
        assert kb.get_pair_by_rsid("rs999999999") is None

    def test_get_pairs_by_gene(self, kb: GeneNutrientKnowledgeBase) -> None:
        mthfr_pairs = kb.get_pairs_by_gene("MTHFR")
        assert len(mthfr_pairs) == 2  # C677T and A1298C
        rsids = {p.variant_rsid for p in mthfr_pairs}
        assert "rs1801133" in rsids
        assert "rs1801131" in rsids

    def test_get_all_tracked_rsids(self, kb: GeneNutrientKnowledgeBase) -> None:
        rsids = kb.get_all_tracked_rsids()
        assert len(rsids) >= 15  # 15 variants across 10 genes
        assert "rs1801133" in rsids
        assert "rs9939609" in rsids

    def test_effect_sizes_have_ci(self, kb: GeneNutrientKnowledgeBase) -> None:
        pair = kb.get_pair_by_rsid("rs1801133")
        assert pair is not None
        assert pair.effect_size.ci_lower < pair.effect_size.value
        assert pair.effect_size.ci_upper > pair.effect_size.value

    def test_allele_frequencies_in_range(
        self, kb: GeneNutrientKnowledgeBase
    ) -> None:
        for rsid in kb.get_all_tracked_rsids():
            pair = kb.get_pair_by_rsid(rsid)
            assert pair is not None
            assert 0 < pair.allele_freq_east_asian < 1, (
                f"Invalid allele freq for {rsid}: {pair.allele_freq_east_asian}"
            )

    def test_recommendation_rules_exist(
        self, kb: GeneNutrientKnowledgeBase
    ) -> None:
        for gene_key in ["MTHFR", "FTO", "APOE", "FADS", "TCF7L2", "VDR"]:
            rules = kb.get_recommendation_rules(gene_key)
            assert rules is not None, f"Missing rules for {gene_key}"
            assert "high_risk" in rules
            assert "low_risk" in rules

    def test_invalid_config_dir_raises(self) -> None:
        with pytest.raises(KnowledgeBaseError):
            GeneNutrientKnowledgeBase(Path("/nonexistent/dir"))

    def test_allele_freq_lookup(self, kb: GeneNutrientKnowledgeBase) -> None:
        freq = kb.get_allele_freq("MTHFR_C677T", "east_asian")
        assert freq is not None
        assert abs(freq - 0.369) < 0.001

    def test_allele_freq_north_south(
        self, kb: GeneNutrientKnowledgeBase
    ) -> None:
        north = kb.get_allele_freq("MTHFR_C677T", "han_chinese_north")
        south = kb.get_allele_freq("MTHFR_C677T", "han_chinese_south")
        assert north is not None and south is not None
        assert north > south  # Known north-south gradient
