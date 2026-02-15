---
paths:
  - "data/**"
  - "src/pipelines/**"
---

# Data Privacy & Ethics Rules

**Context:** This project handles genetic and health data for Chinese farmers. Data privacy is non-negotiable.

---

## 1. PII Protection

- **Never** commit raw data with personally identifiable information (PII)
- All data in `data/` is gitignored by default
- Use anonymized IDs — never real names, ID numbers, or addresses
- Strip PII before any analysis: names, phone numbers, exact birth dates, addresses

## 2. Genetic Data Handling

- Genetic markers stored as coded identifiers, not raw sequences
- SNP data referenced by rs-number, never by individual genome
- Aggregate results only — no individual-level genetic reports in shared outputs

## 3. Health Data

- Health metrics (BMI, blood pressure, etc.) linked only to anonymized IDs
- Dietary intake data aggregated at group level for any shared output
- Medical history never included in version-controlled files

## 4. Data Flow Rules

- Raw data → `data/raw/` (gitignored, never committed)
- Processed data → `data/processed/` (gitignored unless anonymized)
- Only aggregated results and model artifacts in version control
- Document data provenance in `data/README.md`

## 5. Environment Variables

- Database credentials in `.env` (gitignored)
- API keys in environment variables, never in code
- Use `configs/secrets*` pattern — all `secrets*` files are gitignored

## 6. Compliance

- Follow Chinese Personal Information Protection Law (PIPL / 个人信息保护法)
- Informed consent documentation in `docs/ethics/`
- Data retention policies documented
