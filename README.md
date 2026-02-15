# NutriGene AI

Personalized health and nutrition AI system for Chinese agricultural populations, built at China Agricultural University (中国农业大学).

## Overview

NutriGene AI provides personalized nutrition recommendations based on genetic markers and phenotypic data. The system integrates:

- **Genetic analysis** — SNP-based nutrient metabolism profiling
- **Phenotypic assessment** — BMI, blood markers, dietary intake analysis
- **Personalized recommendations** — Tailored to Chinese dietary guidelines (中国居民膳食指南 2022)
- **Statistical analysis** — R-based population health analytics

## Project Structure

```
├── src/                    # Python source code
│   ├── api/                # REST API (FastAPI)
│   ├── models/             # ML models
│   ├── pipelines/          # Data processing
│   └── utils/              # Shared utilities
├── scripts/R/              # R statistical analysis
├── tests/                  # Test suite
├── configs/                # Configuration files
├── notebooks/              # Exploration notebooks
└── docs/                   # Documentation
```

## Getting Started

```bash
# Clone and set up
git clone https://github.com/YOUR_USERNAME/nutrigene-ai.git
cd nutrigene-ai

# Python environment
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Run tests
python -m pytest tests/

# Start API
python src/api/main.py
```

## Development Workflow

This project uses [Claude Code](https://code.claude.com/docs/en/overview) with a plan-first, contractor-mode workflow:

1. Describe a task
2. Claude plans the approach
3. You approve the plan
4. Claude implements, tests, reviews, and verifies autonomously

Quality gates enforce minimum standards (80/100 for commit, 90/100 for PR).

## Data Privacy

This project handles sensitive genetic and health data. See `.claude/rules/data-privacy.md` for data handling rules. Raw data is **never** committed to version control.

## Prerequisites

| Tool | Required For |
|------|-------------|
| Python 3.10+ | Core application |
| R 4.0+ | Statistical analysis |
| [Claude Code](https://code.claude.com/docs/en/overview) | Development workflow |

## License

MIT License.
