from __future__ import annotations

import argparse
import logging

from .app import EyeDentifyApp
from .config import load_config
from .hardware import PiHardware, SimulatedHardware
from .reading import SimulatedReader, TesseractReader
from .speech import ConsoleSpeaker, EspeakSpeaker
from .vision import OpenCVCamera, SimulatedCamera, SimulatedDetector, TFLiteDetector


def build_app(config: dict, simulate: bool = False) -> EyeDentifyApp:
    simulate = simulate or bool(config["runtime"]["simulation"])
    if simulate:
        return EyeDentifyApp(config, SimulatedHardware(), SimulatedCamera(), SimulatedDetector(), SimulatedReader(), ConsoleSpeaker())
    camera_cfg, detection_cfg = config["camera"], config["detection"]
    return EyeDentifyApp(
        config,
        PiHardware(config),
        OpenCVCamera(int(camera_cfg["index"]), int(camera_cfg["width"]), int(camera_cfg["height"])),
        TFLiteDetector(detection_cfg["model"], detection_cfg["labels"], float(detection_cfg["score_threshold"]), int(detection_cfg["max_results"])),
        TesseractReader(config["reading"]["language"]),
        EspeakSpeaker(config["speech"]["rate"], config["speech"]["volume"]),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="EyeDentify assistive-glasses service")
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--simulate", action="store_true")
    parser.add_argument("--once", action="store_true", help="Run one cycle (useful for smoke tests)")
    args = parser.parse_args()
    config = load_config(args.config)
    logging.basicConfig(level=getattr(logging, str(config["runtime"]["log_level"]).upper()), format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    app = build_app(config, args.simulate)
    if args.once:
        app.tick()
        app.camera.close()
        app.hardware.close()
    else:
        app.run()


if __name__ == "__main__":
    main()

