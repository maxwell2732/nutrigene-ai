# Plan: Customize Repo for NutriGene AI

**Status:** COMPLETED
**Date:** 2026-02-15

## Summary

Customized the claude-code-my-workflow repo from academic slides (Beamer/Quarto) to a Python + R health AI project for personalized nutrition.

## Changes Made

- **Deleted 25+ slide-specific files** (10 rules, 7 agents, 12 skills)
- **Created 4 new rules:** python-conventions, data-privacy, health-domain-knowledge, verification-protocol
- **Updated 8 core files:** CLAUDE.md, settings.json, .gitignore, README.md, WORKFLOW_QUICK_REF.md, MEMORY.md, protect-files.sh, quality_score.py
- **Adapted 7 retained files:** quality-gates, r-code-conventions, r-reviewer, domain-reviewer, verifier, data-analysis skill, and 4 other skills (review-r, lit-review, research-ideation, review-paper)
- **Created project directories:** src/api, src/models, src/pipelines, src/utils, scripts/R, tests, configs, notebooks, data
- **Retained core workflow:** plan-first, orchestrator-protocol, session-logging, exploration protocols

## Verification

- No broken references to deleted files
- No slide/Beamer/Quarto terminology in core files
- Valid JSON in settings.json
- No [BRACKETED] placeholders remaining
- All directories exist
