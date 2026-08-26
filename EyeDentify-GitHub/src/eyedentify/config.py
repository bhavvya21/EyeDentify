from __future__ import annotations

from copy import deepcopy
from pathlib import Path

DEFAULTS = {
    "mode": {"switch_gpio": 17, "reading_when_high": True},
    "camera": {"index": 0, "width": 640, "height": 480},
    "detection": {"model": "models/detect.tflite", "labels": "models/labelmap.txt", "score_threshold": 0.55, "announce_cooldown_seconds": 2.5, "center_band": 0.34, "max_results": 5},
    "distance": {"trigger_gpio": 23, "echo_gpio": 24, "max_meters": 4.0, "step_length_meters": 0.75},
    "reading": {"language": "eng", "interval_seconds": 5.0, "min_characters": 3},
    "speech": {"rate": 175, "volume": 100},
    "runtime": {"simulation": False, "log_level": "INFO"},
}


def _merge(base: dict, updates: dict) -> dict:
    for key, value in updates.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            _merge(base[key], value)
        else:
            base[key] = value
    return base


def load_config(path: str | Path | None) -> dict:
    config = deepcopy(DEFAULTS)
    if path:
        import yaml
        with Path(path).open("r", encoding="utf-8") as handle:
            _merge(config, yaml.safe_load(handle) or {})
    return config
