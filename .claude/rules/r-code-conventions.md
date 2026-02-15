---
paths:
  - "**/*.R"
  - "scripts/**/*.R"
---

# R Code Standards

**Standard:** Senior Principal Data Engineer + PhD researcher quality

---

## 1. Reproducibility

- `set.seed()` called ONCE at top (YYYYMMDD format)
- All packages loaded at top via `library()` (not `require()`)
- All paths relative to repository root
- `dir.create(..., recursive = TRUE)` for output directories

## 2. Function Design

- `snake_case` naming, verb-noun pattern
- Roxygen-style documentation
- Default parameters, no magic numbers
- Named return values (lists or tibbles)

## 3. Domain Correctness

- Use Chinese-specific BMI cutoffs (overweight >= 24, obese >= 28)
- Use Chinese DRIs, not Western reference values
- Report effect sizes with 95% CI, not just p-values
- Apply appropriate multiple testing correction
- Document population-specific assumptions

## 4. Visual Identity

```r
# --- China Agricultural University palette ---
cau_green   <- "#006633"
cau_gold    <- "#FFD700"
accent_gray <- "#525252"
positive_green <- "#15803d"
negative_red  <- "#b91c1c"
```

### Custom Theme
```r
theme_nutrigene <- function(base_size = 14) {
  theme_minimal(base_size = base_size) +
    theme(
      plot.title = element_text(face = "bold", color = cau_green),
      legend.position = "bottom"
    )
}
```

### Figure Dimensions
```r
ggsave(filepath, width = 10, height = 6, dpi = 300)
```

## 5. Data Privacy

- Never include raw PII in scripts — use anonymized IDs
- No hardcoded file paths to sensitive data directories
- Aggregated outputs only for any shared results
- Chinese locale support: `Sys.setlocale("LC_ALL", "zh_CN.UTF-8")`

## 6. RDS Data Pattern

**Heavy computations saved as RDS; downstream code loads pre-computed data.**

```r
saveRDS(result, file.path(out_dir, "descriptive_name.rds"))
```

## 7. Common Pitfalls

| Pitfall | Impact | Prevention |
|---------|--------|------------|
| Western BMI cutoffs (25/30) | Misclassification | Use Chinese cutoffs (24/28) |
| Ignoring lactose intolerance | Bad dietary recs | ~90% prevalence in Chinese adults |
| Hardcoded paths | Breaks on other machines | Use relative paths |
| Missing encoding | Garbled Chinese text | Always use UTF-8 |

## 8. Line Length & Mathematical Exceptions

**Standard:** Keep lines <= 100 characters.

**Exception: Mathematical Formulas** -- lines may exceed 100 chars **if and only if:**

1. Breaking the line would harm readability of the math
2. An inline comment explains the mathematical operation
3. The line is in a numerically intensive section

## 9. Code Quality Checklist

```
[ ] Packages at top via library()
[ ] set.seed() once at top
[ ] All paths relative
[ ] Functions documented (Roxygen)
[ ] Figures: explicit dimensions, custom theme
[ ] RDS: every computed object saved
[ ] Comments explain WHY not WHAT
[ ] Chinese-specific reference values used
```
