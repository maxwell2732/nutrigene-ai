---
paths:
  - "src/**/*.py"
  - "tests/**/*.py"
---

# Python Code Standards

**Standard:** Production-grade Python for health AI systems.

---

## 1. Project Structure

- All source code under `src/` with `__init__.py` files
- Tests mirror source structure under `tests/`
- Configuration in `configs/` (YAML/TOML, never hardcoded)
- Entry points in `src/api/main.py` or clearly documented

## 2. Type Hints

- All function signatures must have type hints (params + return)
- Use `typing` module for complex types (`Optional`, `Union`, `List`, `Dict`)
- Use `pydantic` for data models and API schemas

## 3. Testing

- Every public function has at least one test
- Use `pytest` as test framework
- Test files named `test_<module>.py`
- Use fixtures for shared setup
- Mock external services and data sources

## 4. Linting & Formatting

- `ruff` for linting (preferred) or `flake8`
- `black` for formatting (line length 88)
- `mypy` for type checking
- `isort` for import ordering

## 5. Documentation

- Module-level docstrings explaining purpose
- Google-style docstrings for public functions
- Inline comments explain WHY, not WHAT

## 6. Error Handling

- Custom exceptions in `src/utils/exceptions.py`
- Never catch bare `except:`
- Log errors with `logging` module (not `print()`)
- Validate inputs at API boundaries

## 7. Security

- No credentials in code — use environment variables or `configs/secrets*` (gitignored)
- Sanitize all user inputs
- Use parameterized queries for any database access

## 8. Code Quality Checklist

```
[ ] Type hints on all functions
[ ] Tests written and passing
[ ] No hardcoded paths or credentials
[ ] Docstrings on public API
[ ] Logging instead of print()
[ ] ruff/black clean
```
