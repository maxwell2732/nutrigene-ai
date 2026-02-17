"""Genetic risk scoring and dietary recommendation module.

Public API:
    create_engine() — Build a ready-to-use RecommendationEngine.
    generate_report() — One-call shortcut: profile in, report out.
    GeneNutrientKnowledgeBase — Load and query gene-nutrient knowledge.
    RiskScoringEngine — Calculate genetic risk scores.
    RecommendationEngine — Generate personalized dietary recommendations.
    GeneticProfile — Individual genotype data model.
    GeneticRiskReport — Complete risk assessment report.
"""

import sys
from pathlib import Path
from typing import List, Optional

# Enable UTF-8 stdout on Windows so Chinese characters display correctly.
# This must run before any print() calls; does not affect conda run pipes.
if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

from .data_models import (
    DietaryRecommendation,
    EffectSize,
    GeneNutrientPair,
    GeneticProfile,
    GeneticRiskReport,
    RiskScore,
    SNPGenotype,
    Zygosity,
)
from .knowledge_base import GeneNutrientKnowledgeBase
from .recommendation import RecommendationEngine
from .risk_scoring import RiskScoringEngine
from .validators import GeneticDataValidator

# Default config paths (relative to project root)
_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_KB_DIR = _PROJECT_ROOT / "configs" / "gene_nutrient_kb"
_DRI_PATH = _PROJECT_ROOT / "configs" / "chinese_dri.yaml"


def create_engine(
    kb_dir: Optional[Path] = None,
    dri_path: Optional[Path] = None,
) -> RecommendationEngine:
    """Build a ready-to-use RecommendationEngine with default configs.

    Args:
        kb_dir: Path to gene_nutrient_kb/ directory. Defaults to configs/gene_nutrient_kb/.
        dri_path: Path to chinese_dri.yaml. Defaults to configs/chinese_dri.yaml.

    Returns:
        Configured RecommendationEngine.
    """
    kb_dir = kb_dir or _KB_DIR
    dri_path = dri_path or _DRI_PATH
    kb = GeneNutrientKnowledgeBase(kb_dir)
    scorer = RiskScoringEngine(kb)
    return RecommendationEngine(kb, scorer, dri_path)


def generate_report(
    profile: GeneticProfile,
    age: int,
    sex: str,
    traits: Optional[List[str]] = None,
    kb_dir: Optional[Path] = None,
    dri_path: Optional[Path] = None,
) -> GeneticRiskReport:
    """One-call shortcut: profile in, report out.

    Args:
        profile: Individual genetic profile.
        age: Age in years.
        sex: 'male' or 'female'.
        traits: Optional subset of traits; defaults to all.
        kb_dir: Optional override for knowledge base directory.
        dri_path: Optional override for DRI config path.

    Returns:
        Complete GeneticRiskReport.
    """
    engine = create_engine(kb_dir=kb_dir, dri_path=dri_path)
    return engine.generate_report(profile, age, sex, traits)


__all__ = [
    "create_engine",
    "generate_report",
    "DietaryRecommendation",
    "EffectSize",
    "GeneNutrientPair",
    "GeneticDataValidator",
    "GeneticProfile",
    "GeneticRiskReport",
    "GeneNutrientKnowledgeBase",
    "RecommendationEngine",
    "RiskScore",
    "RiskScoringEngine",
    "SNPGenotype",
    "Zygosity",
]
