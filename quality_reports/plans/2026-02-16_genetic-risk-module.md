# Plan: Genetic Risk Module — 10 Gene-Nutrient Pairs

**Status:** COMPLETED
**Date:** 2026-02-16

## Context

NutriGene AI needs its first production Python module: a genetic risk scoring and dietary recommendation engine for 10 well-validated gene-nutrient pairs targeting Chinese populations. All `src/` directories are currently empty. This is greenfield development following established project conventions (type hints, pydantic, pytest, YAML configs, Chinese DRIs, East Asian allele frequencies).

## Approach

**Architecture:** Four-layer module — Data Models → Knowledge Base (YAML) → Risk Scoring → Recommendations. Rule-based v1 (ML-ready for v2).

## Implementation Phases

### Phase 1: Foundation
- `pyproject.toml` — dependencies (pydantic, pyyaml, numpy, scipy, pytest, ruff, mypy)
- `src/utils/exceptions.py` — 6 custom exception classes
- `src/utils/config_loader.py` — YAML loading utility
- `src/models/genetic_risk/data_models.py` — Pydantic models: SNPGenotype, GeneticProfile, EffectSize, GeneNutrientPair, RiskScore, DietaryRecommendation, GeneticRiskReport

### Phase 2: Knowledge Base
- 5 YAML configs in `configs/gene_nutrient_kb/` (genes, variants, allele_frequencies, effect_sizes, recommendations)
- `configs/chinese_dri.yaml` — Chinese DRIs 2022
- `src/models/genetic_risk/knowledge_base.py` — GeneNutrientKnowledgeBase class

### Phase 3: Scoring & Validation
- `src/models/genetic_risk/risk_scoring.py` — Single-gene + polygenic risk scoring with population-normalized z-scores
- `src/models/genetic_risk/validators.py` — Genotype consistency, profile completeness, quality flags

### Phase 4: Recommendations
- `src/models/genetic_risk/recommendation.py` — Maps risk scores to Chinese DRI-based dietary recommendations with Chinese food sources

### Phase 5: Tests
- Full pytest suite mirroring src/ structure
- Test fixtures with sample genotype profiles
- Target: ≥80% coverage

## The 10 Gene-Nutrient Pairs

MTHFR (folate), FTO (energy/obesity), MC4R (satiety), APOE (lipid/fat), FADS1/2 (omega-3/6), TCF7L2 (T2D/carbs), BCMO1 (vitamin A), ADIPOQ (insulin sensitivity), FGF21 (sweet preference), VDR (vitamin D/calcium)

## Verification

All tests pass, coverage ≥80%, ruff clean, imports work, quality score ≥80, end-to-end report generation succeeds.
