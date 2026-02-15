# Workflow Quick Reference

**Model:** Contractor (you direct, Claude orchestrates)
**Project:** NutriGene AI — Personalized Health & Nutrition

---

## The Loop

```
Your instruction
    ↓
[PLAN] (if multi-file or unclear) → Show plan → Your approval
    ↓
[EXECUTE] Implement, test, verify
    ↓
[REPORT] Summary + what's ready
    ↓
Repeat
```

---

## I Ask You When

- **Design forks:** "Option A (fast) vs. Option B (robust). Which?"
- **Data decisions:** "Include this genetic marker? Evidence is mixed."
- **Scope question:** "Also refactor Y while here, or focus on X?"
- **Privacy concern:** "This output might contain PII. Confirm approach?"

---

## I Just Execute When

- Code fix is obvious (bug, pattern application)
- Verification (tests, linting, type checking)
- Documentation (logs, commits)
- Data pipeline steps (per established standards)

---

## Quality Gates (No Exceptions)

| Score | Action |
|-------|--------|
| >= 80 | Ready to commit |
| < 80  | Fix blocking issues |

---

## Non-Negotiables

- **Data privacy:** No PII in version control, ever
- **Type hints:** All Python functions must have type annotations
- **Testing:** Every public function has at least one test
- **Relative paths:** No hardcoded absolute paths
- **Chinese BMI cutoffs:** Overweight >= 24, Obese >= 28 (not 25/30)
- **Chinese DRIs:** Use Chinese dietary reference intakes, not Western

---

## Preferences

**Language:** Python for application code, R for statistical analysis
**Reporting:** Concise bullets, details on request
**Session logs:** Always (post-plan, incremental, end-of-session)
**Data format:** Parquet for large datasets, CSV for small/shareable

---

## Exploration Mode

For experimental work, use the **Fast-Track** workflow:
- Work in `explorations/` folder
- 60/100 quality threshold (vs. 80/100 for production)
- No plan needed — just a research value check (2 min)
- See `.claude/rules/exploration-fast-track.md`

---

## Next Step

You provide task → I plan (if needed) → Your approval → Execute → Done.
