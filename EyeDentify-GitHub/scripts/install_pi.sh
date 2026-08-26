#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

sudo apt update
sudo apt install -y python3-venv python3-opencv python3-picamera2 tesseract-ocr tesseract-ocr-eng espeak-ng liblgpio-dev
python3 -m venv --system-site-packages .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -e '.[pi]'
cp -n config.example.yaml config.yaml
.venv/bin/python scripts/download_model.py
echo "Installed. Edit config.yaml, then run: .venv/bin/eyedentify --simulate --once"

