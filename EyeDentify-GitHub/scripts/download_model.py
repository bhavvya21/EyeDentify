#!/usr/bin/env python3
"""Download Google's Raspberry Pi EfficientDet-Lite0 TFLite model."""
from pathlib import Path
from urllib.request import urlopen

URL = "https://storage.googleapis.com/download.tensorflow.org/models/tflite/task_library/object_detection/rpi/lite-model_efficientdet_lite0_detection_metadata_1.tflite"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "models"


def main():
    OUT.mkdir(exist_ok=True)
    print(f"Downloading {URL}")
    with urlopen(URL, timeout=120) as response:
        data = response.read()
    if len(data) < 1_000_000:
        raise RuntimeError("Downloaded model is unexpectedly small")
    target = OUT / "detect.tflite"
    target.write_bytes(data)
    print(f"Wrote {target} ({len(data):,} bytes)")


if __name__ == "__main__":
    main()
