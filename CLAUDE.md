# CLAUDE.MD -- NutriGene AI Project

**Project:** NutriGene AI — Personalized Health & Nutrition AI
**Institution:** China Agricultural University (中国农业大学)
**Branch:** main

---

## Core Principles

- **Plan first** -- enter plan mode before non-trivial tasks; save plans to `quality_reports/plans/`
- **Verify after** -- run tests and confirm output at the end of every task
- **Quality gates** -- nothing ships below 80/100
- **Data privacy** -- genetic/health data never committed; PII always anonymized
- **[LEARN] tags** -- when corrected, save `[LEARN:category] wrong → right` to MEMORY.md

---

## Folder Structure

```
NutriGene-AI/
├── CLAUDE.md                    # This file
├── .claude/                     # Rules, skills, agents, hooks
├── data/                        # Raw & processed datasets (gitignored)
├── src/                         # Python source code
│   ├── api/                     # Web API (FastAPI/Flask)
│   ├── models/                  # ML/AI models
│   ├── pipelines/               # Data processing pipelines
│   └── utils/                   # Shared utilities
├── scripts/                     # Utility scripts
│   └── R/                       # R statistical analysis
├── notebooks/                   # Jupyter/R notebooks for exploration
├── tests/                       # Test suite
├── configs/                     # Configuration files
├── docs/                        # Documentation & deployment
├── quality_reports/             # Plans, session logs, merge reports
├── explorations/                # Research sandbox
└── templates/                   # Session log, quality report templates
```

---

## Commands

```bash
# Python
python -m pytest tests/
python src/api/main.py
ruff check src/
mypy src/

# R analysis
Rscript scripts/R/analysis.R

# Quality score
python scripts/quality_score.py src/module.py
python scripts/quality_score.py scripts/R/analysis.R
```

---

## Quality Thresholds

| Score | Gate | Meaning |
|-------|------|---------|
| 80 | Commit | Good enough to save |
| 90 | PR | Ready for deployment |
| 95 | Excellence | Aspirational |

---

## Skills Quick Reference

| Command | What It Does |
|---------|-------------|
| `/commit [msg]` | Stage, commit, PR, merge |
| `/review-r [file]` | R code quality review |
| `/data-analysis [dataset]` | End-to-end R/Python analysis |
| `/lit-review [topic]` | Literature search + synthesis |
| `/research-ideation [topic]` | Research questions + strategies |
| `/interview-me [topic]` | Interactive research interview |
| `/review-paper [file]` | Manuscript review |

---

## Key Data Types

| Data Type | Format | Location | Notes |
|-----------|--------|----------|-------|
| Genetic markers | CSV/VCF | `data/raw/` | SNP data, rsIDs |
| Phenotypic data | CSV | `data/raw/` | BMI, blood pressure, etc. |
| Dietary intake | CSV | `data/raw/` | Food frequency questionnaires |
| Processed features | Parquet/CSV | `data/processed/` | Cleaned, anonymized |
| Model artifacts | pickle/joblib | `src/models/saved/` | Trained models |

## Module Status

| Module | Status | Key Functionality |
|--------|--------|-------------------|
| `src/api/` | Planned | REST API for nutrition recommendations |
| `src/models/` | Planned | ML models for personalized nutrition |
| `src/pipelines/` | Planned | Data ingestion and processing |
| `scripts/R/` | Planned | Statistical analysis scripts |

---

## Current Project State

All modules are in planning phase. Core infrastructure (workflow, quality gates, review agents) is configured and ready.
