"""Tests for YAML config loader utility."""

from pathlib import Path

import pytest

from src.utils.config_loader import load_yaml_config
from src.utils.exceptions import ConfigValidationError

CONFIGS_DIR = Path(__file__).parent.parent.parent / "configs"


def test_load_valid_yaml() -> None:
    """Loading a valid YAML file returns a dict."""
    result = load_yaml_config(CONFIGS_DIR / "chinese_dri.yaml")
    assert isinstance(result, dict)
    assert "folate" in result
    assert "energy" in result


def test_load_nonexistent_file() -> None:
    """Loading a nonexistent file raises ConfigValidationError."""
    with pytest.raises(ConfigValidationError, match="not found"):
        load_yaml_config(Path("/nonexistent/path.yaml"))


def test_load_genes_yaml() -> None:
    """genes.yaml loads with expected gene entries."""
    result = load_yaml_config(CONFIGS_DIR / "gene_nutrient_kb" / "genes.yaml")
    assert "MTHFR" in result
    assert "FTO" in result
    assert len(result) >= 10


def test_dri_has_required_nutrients() -> None:
    """Chinese DRI config has all expected nutrients."""
    dri = load_yaml_config(CONFIGS_DIR / "chinese_dri.yaml")
    required = ["energy", "folate", "vitamin_a", "vitamin_d", "calcium", "iron"]
    for nutrient in required:
        assert nutrient in dri, f"Missing nutrient: {nutrient}"
        assert "unit" in dri[nutrient], f"Missing unit for {nutrient}"
