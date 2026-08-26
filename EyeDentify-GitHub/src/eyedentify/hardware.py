from __future__ import annotations

import logging
import random

from .core import Mode

LOG = logging.getLogger(__name__)


class PiHardware:
    def __init__(self, config: dict):
        try:
            from gpiozero import Button, DistanceSensor
        except ImportError as exc:
            raise RuntimeError("GPIO libraries missing; install the Raspberry Pi dependencies or use --simulate") from exc
        mode_cfg, distance_cfg = config["mode"], config["distance"]
        self.reading_when_high = bool(mode_cfg["reading_when_high"])
        self.switch = Button(int(mode_cfg["switch_gpio"]), pull_up=False, bounce_time=0.05)
        self.sensor = DistanceSensor(
            echo=int(distance_cfg["echo_gpio"]),
            trigger=int(distance_cfg["trigger_gpio"]),
            max_distance=float(distance_cfg["max_meters"]),
            queue_len=5,
        )

    def mode(self) -> Mode:
        high = self.switch.is_pressed
        return Mode.READ if high == self.reading_when_high else Mode.DETECT

    def distance_m(self) -> float | None:
        # gpiozero DistanceSensor.distance is already expressed in meters.
        value = float(self.sensor.distance)
        return value if value > 0 else None

    def close(self) -> None:
        self.switch.close()
        self.sensor.close()


class SimulatedHardware:
    def __init__(self, initial_mode: Mode = Mode.DETECT, distance_m: float = 1.5):
        self.current_mode = initial_mode
        self.current_distance = distance_m

    def mode(self) -> Mode:
        return self.current_mode

    def distance_m(self) -> float:
        return max(0.2, self.current_distance + random.uniform(-0.05, 0.05))

    def close(self) -> None:
        pass
