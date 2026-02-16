"""Shared test fixtures for NutriGene AI."""

from pathlib import Path

import pytest

from src.models.genetic_risk.data_models import GeneticProfile, SNPGenotype, Zygosity
from src.models.genetic_risk.knowledge_base import GeneNutrientKnowledgeBase
from src.models.genetic_risk.risk_scoring import RiskScoringEngine
from src.utils.config_loader import load_yaml_config

FIXTURES_DIR = Path(__file__).parent / "models" / "genetic_risk" / "fixtures"
CONFIGS_DIR = Path(__file__).parent.parent / "configs"
KB_DIR = CONFIGS_DIR / "gene_nutrient_kb"


@pytest.fixture
def kb() -> GeneNutrientKnowledgeBase:
    """Load the gene-nutrient knowledge base."""
    return GeneNutrientKnowledgeBase(KB_DIR)


@pytest.fixture
def scorer(kb: GeneNutrientKnowledgeBase) -> RiskScoringEngine:
    """Create a scoring engine."""
    return RiskScoringEngine(kb)


def _load_profile(name: str) -> GeneticProfile:
    """Load a test profile from fixtures YAML."""
    data = load_yaml_config(FIXTURES_DIR / "sample_genotypes.yaml")
    raw = data[name]
    genotypes = [SNPGenotype(**g) for g in raw["genotypes"]]
    return GeneticProfile(
        individual_id=raw["individual_id"],
        population=raw["population"],
        data_source=raw["data_source"],
        genotypes=genotypes,
    )


@pytest.fixture
def high_risk_profile() -> GeneticProfile:
    """High-risk test profile (homozygous risk alleles)."""
    return _load_profile("individual_high_risk")


@pytest.fixture
def moderate_risk_profile() -> GeneticProfile:
    """Moderate-risk test profile (mostly heterozygous)."""
    return _load_profile("individual_moderate_risk")


@pytest.fixture
def low_risk_profile() -> GeneticProfile:
    """Low-risk test profile (homozygous protective alleles)."""
    return _load_profile("individual_low_risk")


@pytest.fixture
def partial_profile() -> GeneticProfile:
    """Partial test profile (only MTHFR, low quality)."""
    return _load_profile("individual_partial")
