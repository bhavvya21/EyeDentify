from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import math


class Mode(str, Enum):
    DETECT = "detect"
    READ = "read"


@dataclass(frozen=True)
class Detection:
    label: str
    score: float
    xmin: float
    ymin: float
    xmax: float
    ymax: float

    @property
    def center_x(self) -> float:
        return (self.xmin + self.xmax) / 2.0


def horizontal_position(center_x: float, center_band: float = 0.34) -> str:
    """Map normalized x coordinate to an accessible direction phrase."""
    half = center_band / 2.0
    if center_x < 0.5 - half:
        return "to your left"
    if center_x > 0.5 + half:
        return "to your right"
    return "in front"


def meters_to_steps(distance_m: float | None, step_length_m: float = 0.75) -> int | None:
    if distance_m is None or not math.isfinite(distance_m) or distance_m <= 0:
        return None
    return max(1, int(round(distance_m / step_length_m)))


def navigation_message(detection: Detection, distance_m: float | None, step_length_m: float, center_band: float) -> str:
    direction = horizontal_position(detection.center_x, center_band)
    steps = meters_to_steps(distance_m, step_length_m)
    if steps is None:
        return f"{detection.label} {direction}."
    unit = "step" if steps == 1 else "steps"
    return f"{detection.label} {steps} {unit} away, {direction}."

