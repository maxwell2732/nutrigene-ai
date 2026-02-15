---
name: data-analysis
description: End-to-end data analysis workflow for health/nutrition data using R or Python
disable-model-invocation: true
argument-hint: "[dataset path or description of analysis goal]"
allowed-tools: ["Read", "Grep", "Glob", "Write", "Edit", "Bash", "Task"]
---

# Data Analysis Workflow

Run an end-to-end data analysis: load, explore, analyze, and produce publication-ready output.

**Input:** `$ARGUMENTS` — a dataset path (e.g., `data/processed/cohort.csv`) or a description of the analysis goal (e.g., "analyze BMI distribution by genotype group").

---

## Constraints

- **Follow code conventions** in `.claude/rules/r-code-conventions.md` (R) or `.claude/rules/python-conventions.md` (Python)
- **Data privacy:** Never include PII in outputs — use anonymized data only
- **Use Chinese-specific reference values:** BMI cutoffs (24/28), Chinese DRIs
- **Save all scripts** to `scripts/R/` (R) or `src/pipelines/` (Python)
- **Save all outputs** (figures, tables, RDS/pickle) to `output/`
- **Run r-reviewer** (R) or verify with tests (Python) before presenting results

---

## Workflow Phases

### Phase 1: Setup and Data Loading

1. Read relevant code conventions for project standards
2. Create script with proper header (title, author, purpose, inputs, outputs)
3. Load required packages at top
4. Set seed once at top: `set.seed(42)` (R) or `random.seed(42)` (Python)
5. Load and inspect the dataset — check for PII before proceeding

### Phase 2: Exploratory Data Analysis

Generate diagnostic outputs:
- **Summary statistics:** distributions, missingness rates, variable types
- **Distributions:** Histograms for key continuous variables (BMI, nutrients, etc.)
- **Relationships:** Scatter plots, correlation matrices
- **Group comparisons:** By genotype, age group, region, etc.
- **Data quality:** Outlier detection, encoding validation (UTF-8 for Chinese text)

Save all diagnostic figures to `output/diagnostics/`.

### Phase 3: Main Analysis

Based on the research question:
- **Statistical analysis:** Appropriate tests for data type and research question
- **Multiple testing:** Apply correction (Bonferroni, FDR) when testing many associations
- **Effect sizes:** Report with 95% CI alongside raw coefficients
- **Subgroup analysis:** Consider age, sex, region, and other relevant stratifications
- **Use Chinese reference values:** BMI cutoffs, DRIs, population-specific allele frequencies

### Phase 4: Publication-Ready Output

**Tables:**
- Use `modelsummary` (R) or formatted DataFrames (Python) for results tables
- Include all standard elements: estimates, CIs, p-values, N
- Export as `.csv` and formatted output

**Figures:**
- Use project theme (`theme_nutrigene` in R, or consistent matplotlib/seaborn style)
- Include proper axis labels (sentence case, units)
- Export with explicit dimensions
- Save as both `.pdf` and `.png`

### Phase 5: Save and Review

1. Save all key objects (`saveRDS()` in R, `pickle/joblib` in Python)
2. Create `output/` subdirectories as needed
3. Run the appropriate reviewer agent
4. Address any Critical or High issues from the review

---

## Important

- **Data privacy first.** Check for PII before any analysis.
- **Reproduce, don't guess.** If the user specifies an analysis, run exactly that.
- **Show your work.** Print summary statistics before jumping to models.
- **Use relative paths.** All paths relative to repository root.
- **No hardcoded values.** Use variables for sample restrictions, thresholds, etc.
- **Chinese context.** Use Chinese-specific reference values and conventions.
