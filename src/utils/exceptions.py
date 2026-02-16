"""Custom exceptions for NutriGene AI."""


class NutriGeneError(Exception):
    """Base exception for NutriGene AI."""


class KnowledgeBaseError(NutriGeneError):
    """Knowledge base loading or validation error."""


class ConfigValidationError(NutriGeneError):
    """Configuration file validation error."""


class RiskScoringError(NutriGeneError):
    """Risk score calculation error."""


class RecommendationError(NutriGeneError):
    """Recommendation generation error."""


class GeneticDataValidationError(NutriGeneError):
    """Genetic data validation error."""
