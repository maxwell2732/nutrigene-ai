"""Genetic risk scoring and dietary recommendation module.

Public API:
    GeneNutrientKnowledgeBase — Load and query gene-nutrient knowledge.
    RiskScoringEngine — Calculate genetic risk scores.
    RecommendationEngine — Generate personalized dietary recommendations.
    GeneticProfile — Individual genotype data model.
    GeneticRiskReport — Complete risk assessment report.
"""

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

__all__ = [
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
