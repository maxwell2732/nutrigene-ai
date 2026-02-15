---
paths:
  - "src/models/**"
  - "scripts/R/**"
---

# Health & Nutrition Domain Knowledge

**Project:** Personalized nutrition recommendations based on genetic/phenotypic data for Chinese agricultural populations.

---

## 1. Chinese Dietary Guidelines (中国居民膳食指南 2022)

- Reference standard for nutritional recommendations
- Daily reference intakes (DRIs) specific to Chinese populations
- Consider regional dietary patterns (northern vs. southern, urban vs. rural)

## 2. Nutrient Units & Conventions

| Nutrient | Unit | Notes |
|----------|------|-------|
| Energy | kcal or kJ | 1 kcal = 4.184 kJ |
| Macronutrients | g | Protein, fat, carbohydrate |
| Vitamins | mg or μg | Depends on vitamin type |
| Minerals | mg or μg | Iron, zinc, calcium, etc. |
| BMI | kg/m² | Chinese cutoffs differ: overweight ≥ 24, obese ≥ 28 |

## 3. Genetic Marker Handling

- SNPs referenced by rsID (e.g., rs1801133 for MTHFR C677T)
- Gene-nutrient interactions must cite peer-reviewed evidence
- Effect sizes reported with confidence intervals
- Population-specific allele frequencies (use East Asian reference panels)

## 4. Statistical Conventions

- Report effect sizes with 95% CI, not just p-values
- Use appropriate multiple testing correction (Bonferroni, FDR)
- Distinguish association from causation explicitly
- Sample size justification required for all analyses

## 5. Chinese Locale Handling

- Support UTF-8 encoding for Chinese characters (人名、地名、食物名)
- Date format: YYYY-MM-DD (ISO 8601)
- Number formatting: use standard (1,000.00), not Chinese (1.000,00)

## 6. Known Pitfalls

| Pitfall | Impact | Prevention |
|---------|--------|------------|
| Using Western BMI cutoffs | Misclassification | Use Chinese-specific cutoffs (24/28) |
| Ignoring lactose intolerance prevalence | Bad recommendations | ~90% prevalence in Chinese adults |
| Western dietary reference values | Inappropriate targets | Use Chinese DRIs |
| Missing rare alleles in East Asian populations | Wrong risk scores | Use gnomAD East Asian frequencies |
