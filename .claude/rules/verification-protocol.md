---
paths:
  - "src/**"
  - "scripts/**"
  - "tests/**"
---

# Task Completion Verification Protocol

**At the end of EVERY task, Claude MUST verify the output works correctly.** This is non-negotiable.

## For Python Modules:

1. Run `python -m pytest tests/` (or specific test file)
2. Run `ruff check src/` for linting
3. Run `mypy src/` for type checking (if configured)
4. Verify no import errors: `python -c "import src.module"`
5. Report pass/fail results

## For API Endpoints:

1. Start the server (if not running)
2. Test endpoint with a sample request
3. Verify response status code and schema
4. Check error handling with invalid input

## For R Scripts:

1. Run `Rscript scripts/R/filename.R`
2. Verify output files were created with non-zero size
3. Spot-check results for reasonable values

## For Data Pipelines:

1. Run pipeline with sample/test data
2. Verify output schema matches expectations
3. Check row counts and basic statistics
4. Validate no PII leakage in outputs

## Verification Checklist:

```
[ ] All tests pass
[ ] No linting errors
[ ] Output files created successfully
[ ] No hardcoded paths or credentials
[ ] Data privacy rules respected
[ ] Results are reasonable (sanity check)
[ ] Reported results to user
```
