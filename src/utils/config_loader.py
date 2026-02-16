"""Configuration file loading utilities."""

import logging
from pathlib import Path
from typing import Any, Dict

import yaml

from .exceptions import ConfigValidationError

logger = logging.getLogger(__name__)


def load_yaml_config(config_path: Path) -> Dict[str, Any]:
    """Load and parse a YAML configuration file.

    Args:
        config_path: Path to YAML file.

    Returns:
        Parsed configuration dictionary.

    Raises:
        ConfigValidationError: If file not found or invalid YAML.
    """
    if not config_path.exists():
        raise ConfigValidationError(f"Config file not found: {config_path}")

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ConfigValidationError(f"Invalid YAML in {config_path}: {e}") from e

    if config is None:
        raise ConfigValidationError(f"Empty config file: {config_path}")

    logger.debug("Loaded config from %s", config_path)
    return config
