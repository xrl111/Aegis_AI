"""Aegis AI — Centralized Configuration.

Load thresholds and constants from config.yaml.
All magic numbers MUST be defined here, not in module code.
"""

from pathlib import Path
from typing import Any

import yaml


_CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "config.yaml"

_cache: dict[str, Any] | None = None


def _load() -> dict[str, Any]:
    global _cache
    if _cache is None:
        with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
            _cache = yaml.safe_load(f)
    return _cache


def get(section: str, key: str) -> Any:
    """Get a config value.  Example: ``get("thresholds", "grade_z_threshold")``."""
    return _load()[section][key]


def reload() -> None:
    """Force reload config from disk (useful in tests)."""
    global _cache
    _cache = None


# ── Convenience accessors ─────────────────────────────────────

# Thresholds
GRADE_Z_THRESHOLD: float = get("thresholds", "grade_z_threshold")
ATTENDANCE_Z_THRESHOLD: float = get("thresholds", "attendance_z_threshold")
SUBMISSION_Z_THRESHOLD: float = get("thresholds", "submission_z_threshold")
PERSISTENCE_COUNT: int = get("thresholds", "persistence_count")
SEASONAL_RATIO: float = get("thresholds", "seasonal_ratio")

# Baseline
WINDOW_SIZE: int = get("baseline", "window_size")
MAD_FLOOR: float = get("baseline", "mad_floor")
MIN_WINDOW_RATIO: float = get("baseline", "min_window_ratio")

# Data gate
MIN_GRADE_POINTS: int = get("data_gate", "min_grade_points")
MIN_ATTENDANCE_POINTS: int = get("data_gate", "min_attendance_points")
MIN_SUBMISSION_POINTS: int = get("data_gate", "min_submission_points")

# Alert
COOLDOWN_DAYS: int = get("alert", "cooldown_days")
EXPIRY_DAYS: int = get("alert", "expiry_days")
META_ALERT_THRESHOLD: int = get("alert", "meta_alert_threshold")

# Fusion
MIN_SIGNALS_FOR_ALERT: int = get("fusion", "min_signals_for_alert")
MIN_ACTIVE_SIGNALS: int = get("fusion", "min_active_signals")
