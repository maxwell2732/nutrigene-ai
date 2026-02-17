# Genetic Risk Module — Developer Guide

**Module:** `src/models/genetic_risk/`
**Status:** Complete (v0.1)
**Last updated:** 2026-02-17

---

## Overview

The genetic risk module is NutriGene AI's first production Python component. It scores genetic risk for 10 well-validated gene-nutrient pairs and generates personalized dietary recommendations calibrated to Chinese Dietary Reference Intakes (DRIs, 2022) and East Asian allele frequencies.

Architecture: **rule-based v1**, designed to be ML-ready for v2.

---

## The 10 Gene-Nutrient Pairs

| Gene | Nutrient | Key SNPs |
|------|----------|----------|
| MTHFR | Folate | rs1801133 (C677T), rs1801131 (A1298C) |
| FTO | Energy balance / obesity | rs9939609 |
| MC4R | Satiety / energy balance | rs17782313, rs12970134 |
| APOE | Dietary fat / lipids | rs429358, rs7412 |
| FADS1/2 | Omega-3 / Omega-6 | rs174547, rs498793 |
| TCF7L2 | Carbohydrate / T2D risk | rs7903146 |
| BCMO1 | Vitamin A (beta-carotene) | rs12934922 |
| ADIPOQ | Insulin sensitivity | rs1501299 |
| FGF21 | Macronutrient preference | rs838133 |
| VDR | Vitamin D / Calcium | rs2228570 (FokI), rs1544410 (BsmI) |

**Total:** 15 SNP variants across 10 genes.

---

## Module Structure

```
src/models/genetic_risk/
├── __init__.py           # Public API: create_engine, generate_report
├── data_models.py        # Pydantic models (SNPGenotype, GeneticProfile, RiskScore, ...)
├── knowledge_base.py     # Loads YAML configs; lookup by rsID / gene
├── risk_scoring.py       # Single-gene + polygenic scoring, z-score percentiles
├── recommendation.py     # Maps risk scores to DRI-based dietary recommendations
└── validators.py         # Genotype consistency and quality flag checks

configs/gene_nutrient_kb/
├── genes.yaml            # Gene metadata
├── variants.yaml         # SNP definitions (rsID, risk/protective alleles, evidence)
├── effect_sizes.yaml     # Effect sizes with 95% CIs (per risk allele, additive model)
├── allele_frequencies.yaml  # Risk allele frequencies (East Asian, Han North/South, global)
└── recommendations.yaml  # Recommendation rules by risk tier

configs/
└── chinese_dri.yaml      # Chinese DRIs 2022 (folate, vitamin D, calcium, omega-3, ...)
```

---

## Setup

The module requires **Python 3.10+**. Use the `gnn` conda environment:

```bash
conda activate gnn
cd C:\Users\zhuch\my-project
pip install pydantic pyyaml pytest pytest-cov ruff
```

---

## Running the Tests

```bash
# Run all 69 tests
python -m pytest tests/ -v

# Run with coverage report
python -m pytest tests/ --cov=src --cov-report=term-missing

# Lint check
python -m ruff check src/ tests/
```

**Expected results:**

| Check | Result |
|-------|--------|
| Tests | 69/69 passed |
| Ruff | Clean |
| Coverage (overall) | 88% |
| Coverage (`validators.py`) | 42% — defensive paths, not triggered in normal flows |

---

## Public API

The module exposes two convenience functions for quick usage:

```python
from src.models.genetic_risk import create_engine, generate_report

# Option 1: One-call shortcut (creates engine internally each time)
report = generate_report(profile, age=35, sex="female")

# Option 2: Reusable engine (better for batch processing)
engine = create_engine()
report1 = engine.generate_report(profile1, age=35, sex="female")
report2 = engine.generate_report(profile2, age=50, sex="male")
```

Both functions auto-discover config paths (`configs/gene_nutrient_kb/` and `configs/chinese_dri.yaml`). Override with `kb_dir=` and `dri_path=` if needed.

For lower-level access, import the classes directly: `GeneNutrientKnowledgeBase`, `RiskScoringEngine`, `RecommendationEngine`.

---

## Quick Smoke Test

Paste this into a Python shell to generate an end-to-end report:

```python
from src.models.genetic_risk import create_engine, generate_report
from src.models.genetic_risk.data_models import GeneticProfile, SNPGenotype

# High-risk MTHFR + FTO profile for a 35-year-old woman
profile = GeneticProfile(genotypes=[
    SNPGenotype(rsid="rs1801133", genotype="TT", chromosome="1",  position=11856378),
    SNPGenotype(rsid="rs9939609", genotype="AA", chromosome="16", position=53820527),
])

report = generate_report(profile, age=35, sex="female")
print(report.summary())
```

This creates a worst-case MTHFR (TT homozygous risk) + FTO (AA homozygous risk) profile and prints a personalized nutrition recommendation summary with Chinese DRI targets and food sources.

---

## What Was Fixed

### 2026-02-17 (round 2): Smoke test didn't work

The Quick Smoke Test above was documented but never actually run. Three issues:

1. **`create_engine()` / `generate_report()` didn't exist** — documented in `__init__.py` docstring but never implemented. Added as convenience functions that auto-discover config paths.
2. **`GeneticRiskReport.summary()` didn't exist** — added a human-readable summary method that prints risk scores, recommendations with food sources, and missing variants.
3. **`SNPGenotype` / `GeneticProfile` required too many fields** — `reference_allele`, `alternate_allele`, `zygosity`, `individual_id`, and `data_source` were all required with no defaults, making the minimal smoke test constructor fail. Made these optional with sensible defaults (`"N"`, `Zygosity.UNKNOWN`, `"anonymous"`, `"unknown"`).

### 2026-02-17 (round 1): Test and lint fixes

The module was built on 2026-02-16 but not verified. The following issues were found and resolved:

1. **Missing SNP variant** — knowledge base had 14 variants; test asserted `>= 15`. Added **VDR BsmI (`rs1544410`)**.
2. **Unused imports** — Ruff flagged 5 unused imports; auto-fixed with `ruff --fix`.

---

## Key Design Decisions

- **Additive model** — effect sizes are per risk allele; homozygous risk = 2× effect.
- **APOE special case** — epsilon genotype (e2/e3/e4) is inferred from the combination of rs429358 and rs7412, not treated as a simple additive SNP.
- **Polygenic scoring** — traits with multiple SNPs (obesity: FTO + MC4R) use population-normalized z-scores to combine effects.
- **Partial profiles** — missing variants are handled gracefully; scoring proceeds with available data and flags gaps in the report.
- **Chinese DRI calibration** — recommendations are age-group and sex-specific, following the 2022 Chinese DRI revision.

---

## Next Steps (v0.2 candidates)

- Increase `validators.py` test coverage (currently 42%)
- Add REST API endpoint (`src/api/`) to expose `generate_report`
- Integrate dietary intake data for gene × diet interaction scoring
- Expand to additional SNPs (VDR TaqI, PPARG Pro12Ala, etc.)
