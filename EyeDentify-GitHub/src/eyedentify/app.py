from __future__ import annotations

import logging
import signal
import time

from .core import Mode, navigation_message

LOG = logging.getLogger(__name__)


class EyeDentifyApp:
    def __init__(self, config, hardware, camera, detector, reader, speaker, clock=time.monotonic):
        self.config, self.hardware, self.camera = config, hardware, camera
        self.detector, self.reader, self.speaker, self.clock = detector, reader, speaker, clock
        self.running = True
        self.last_announced: dict[str, float] = {}
        self.last_read = float("-inf")
        self.previous_mode = None

    def stop(self, *_args) -> None:
        self.running = False

    def _announce_detection(self, frame, now: float) -> None:
        cfg = self.config["detection"]
        for detection in self.detector.detect(frame):
            last = self.last_announced.get(detection.label, float("-inf"))
            if now - last < float(cfg["announce_cooldown_seconds"]):
                continue
            message = navigation_message(detection, self.hardware.distance_m(), self.config["distance"]["step_length_meters"], cfg["center_band"])
            self.speaker.say(message)
            self.last_announced[detection.label] = now
            break

    def _announce_reading(self, frame, now: float) -> None:
        cfg = self.config["reading"]
        if now - self.last_read < float(cfg["interval_seconds"]):
            return
        text = self.reader.read(frame)
        self.last_read = now
        if len(text) >= int(cfg["min_characters"]):
            self.speaker.say(text)
        else:
            self.speaker.say("No readable text found.")

    def tick(self) -> None:
        mode = self.hardware.mode()
        if mode != self.previous_mode:
            self.speaker.say("Reading mode." if mode is Mode.READ else "Detection mode.")
            self.previous_mode = mode
        frame = self.camera.frame()
        now = self.clock()
        if mode is Mode.READ:
            self._announce_reading(frame, now)
        else:
            self._announce_detection(frame, now)

    def run(self) -> None:
        signal.signal(signal.SIGTERM, self.stop)
        signal.signal(signal.SIGINT, self.stop)
        try:
            while self.running:
                try:
                    self.tick()
                except Exception:
                    LOG.exception("Runtime cycle failed")
                    time.sleep(0.5)
        finally:
            self.camera.close()
            self.hardware.close()

