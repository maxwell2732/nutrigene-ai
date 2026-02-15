---
paths:
  - "src/**/*.py"
  - "tests/**/*.py"
  - "scripts/**/*.R"
---

# Quality Gates & Scoring Rubrics

## Thresholds

- **80/100 = Commit** -- good enough to save
- **90/100 = PR** -- ready for deployment
- **95/100 = Excellence** -- aspirational

## Python Modules (.py)

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | Import/syntax errors | -100 |
| Critical | Missing type hints on public functions | -15 |
| Critical | No tests for public API | -15 |
| Critical | Hardcoded credentials or PII | -20 |
| Major | Missing error handling at API boundaries | -5 |
| Major | No input validation on external data | -5 |
| Major | Hardcoded absolute paths | -5 |
| Minor | Missing docstrings | -1 per function |
| Minor | Long lines (>88 chars, black standard) | -1 |

## API Endpoints

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | Endpoint returns 500 on valid input | -100 |
| Critical | No input validation (Pydantic) | -20 |
| Critical | PII in response without authorization | -20 |
| Major | Missing error response schemas | -5 |
| Major | No logging on errors | -3 |
| Minor | Missing OpenAPI documentation | -2 |

## Data Pipelines

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | Pipeline fails on sample data | -100 |
| Critical | PII leakage in output | -20 |
| Major | No data validation/schema check | -10 |
| Major | Missing logging/audit trail | -5 |
| Minor | No progress reporting | -1 |

## R Scripts (.R)

| Severity | Issue | Deduction |
|----------|-------|-----------|
| Critical | Syntax errors | -100 |
| Critical | Domain-specific bugs | -30 |
| Critical | Hardcoded absolute paths | -20 |
| Major | Missing set.seed() | -10 |
| Major | Missing figure generation | -5 |

## Enforcement

- **Score < 80:** Block commit. List blocking issues.
- **Score < 90:** Allow commit, warn. List recommendations.
- User can override with justification.

## Quality Reports

Generated **only at merge time**. Use `templates/quality-report.md` for format.
Save to `quality_reports/merges/YYYY-MM-DD_[branch-name].md`.

## Tolerance Thresholds (Research)

| Quantity | Tolerance | Rationale |
|----------|-----------|-----------|
| Nutrient estimates | 0.1 mg | Measurement precision |
| Risk scores | 0.01 | Model calibration |
| P-values | Report exact | No rounding to significance |
