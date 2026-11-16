# Eyedentify

Assistive glasses powered by Raspberry Pi 5, with a companion web workspace for visual context and spoken reading.

[Open the Eyedentify workspace](https://eyedentify-senseai.me-ed0430495.chatgpt.site) · [Circuit diagram](docs/hardware/eyedentify-circuit.png) · [Website documentation](docs/WEBSITE.md)

The hosted workspace currently requires its owner's ChatGPT account. The Raspberry Pi software runs separately from the website; a live telemetry connection is not yet implemented.

## Website

- Overview and Eyedentify dashboard with empty observation panels until hardware data is available.
- Permission-based browser camera preview; frames are not uploaded or recorded by the app.
- Reading studio with pasted text, `.txt` import, browser speech and adjustable reading speed.
- Session-history interface, currently empty without a connected data source.
- Larger text, higher contrast and reduced-motion preferences stored in the browser.

Browser camera preview does not perform object detection or OCR. The device runtime below supplies those capabilities on the Raspberry Pi. Environmental audio classification and IMU readings require additional hardware/software integration.

### Overview

![Eyedentify overview with assistive-glasses artwork and dashboard navigation](docs/screenshots/01-overview.png)

### Visual context and sensor workspace

![Eyedentify visual context panel and separate audio, proximity and movement areas](docs/screenshots/02-context-dashboard.png)

These supplied screenshots capture an earlier UI revision. The Device setup navigation entry and hardware shortcut shown in them have since been removed from the hosted website. Unconnected sensor fields remain empty.

## Raspberry Pi software

Raspberry Pi 5 software for dual-mode assistive glasses:

- **Detection mode:** camera-based COCO object recognition, left/center/right positioning, and HC-SR04 distance converted to an approximate step count.
- **Reading mode:** camera capture, image cleanup, Tesseract OCR, and offline speech.
- **Accessible control:** a physical slide switch changes modes while the process is running.
- **Audio:** offline `espeak-ng`; Raspberry Pi OS routes it to the selected Bluetooth or wired audio output.

> Safety: this is an assistive prototype, not a certified mobility aid. It can miss or misidentify obstacles. Do not use it as the sole navigation aid or near traffic, stairs, platforms, or other hazards.

## Hardware

- Raspberry Pi 5 (4 GB or 8 GB) with Raspberry Pi OS 64-bit
- USB UVC webcam (the default code uses `/dev/video0`)
- HC-SR04 ultrasonic sensor
- SPDT slide switch
- Bluetooth speaker or bone-conduction headset
- Stable 5 V / 5 A Pi 5 supply or suitable USB-C power bank

### Circuit diagram

![Eyedentify circuit: Raspberry Pi 5, USB camera, HC-SR04 with ECHO voltage divider, mode switch, Bluetooth audio and USB-C power](docs/hardware/eyedentify-circuit.png)

This is a functional wiring diagram, not a physical header orientation guide. Pin numbers below are physical header positions; GPIO names use BCM numbering. Wire crossings without junction dots are not connected. The slide switch common goes to GPIO17; one throw goes to 3.3 V and the other is left unconnected. The software enables GPIO17's internal pull-down.

References: [Raspberry Pi GPIO documentation](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html) and [GPIO Zero distance-sensor wiring](https://gpiozero.readthedocs.io/en/rtd/api_input.html#distancesensor).

### Wiring (BCM numbering)

| Device | Raspberry Pi |
|---|---|
| Slide switch common | GPIO17 (pin 11) |
| Slide switch other side | 3.3 V (pin 1) |
| HC-SR04 VCC | 5 V (pin 2) |
| HC-SR04 GND | GND (pin 6) |
| HC-SR04 TRIG | GPIO23 (pin 16) |
| HC-SR04 ECHO | GPIO24 (pin 18), **through a 5 V-to-3.3 V divider/level shifter** |

Never connect HC-SR04 ECHO directly to a Pi GPIO; its 5 V output can damage the Pi. A common divider is 1 kΩ from ECHO to GPIO24 and 2 kΩ from GPIO24 to GND.

## Install on Raspberry Pi 5

```bash
git clone https://github.com/bhavvya21/EyeDentify.git
cd EyeDentify/EyeDentify-GitHub
chmod +x scripts/install_pi.sh
./scripts/install_pi.sh
```

If `tflite-runtime` has no wheel for your Raspberry Pi OS Python version, install Google's current LiteRT wheel and rerun the install:

```bash
.venv/bin/pip install ai-edge-litert
```

Edit `config.yaml` if your GPIO pins or camera index differ. Then verify software without hardware:

```bash
.venv/bin/eyedentify --config config.yaml --simulate --once
```

Expected output includes `Detection mode` and a simulated person announcement.

## Hardware checks before wearing

```bash
# Camera
v4l2-ctl --list-devices
.venv/bin/python -c "import cv2; c=cv2.VideoCapture(0); print(c.isOpened(), c.read()[0]); c.release()"

# OCR
tesseract --version
# For a real OCR check, provide an image containing text:
tesseract /path/to/text-image.png stdout

# Audio (pair/select the Bluetooth device in Raspberry Pi OS first)
espeak-ng 'EyeDentify audio test'

# One real runtime cycle
.venv/bin/eyedentify --config config.yaml --once
```

Check the measured distance against a tape measure at 0.5 m, 1 m, and 2 m. Tune `distance.step_length_meters` for the user. Confirm switch orientation; reverse `mode.reading_when_high` if needed. Test indoors with a sighted assistant before any controlled outdoor trial.

## Run automatically at boot

The supplied service uses user `pi` and paths under `/home/pi/EyeDentify`. This repository stores the Python application in `EyeDentify-GitHub/`: update the service's `WorkingDirectory` to `/home/pi/EyeDentify/EyeDentify-GitHub`, and update `ExecStart` to use that folder's `.venv/bin/eyedentify` executable and `config.yaml` file. Use your actual username and checkout path before enabling it.

```bash
sudo cp systemd/eyedentify.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now eyedentify
journalctl -u eyedentify -f
```

## Development and tests

```bash
python -m venv .venv
.venv/bin/pip install -e '.[dev]'
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/eyedentify --config config.example.yaml --simulate --once
```

The automated suite tests direction mapping, distance-to-step conversion, message composition, mode switching, OCR-mode output, and repeat-announcement cooldown without requiring Pi hardware.

## Repository map

Application paths below are relative to `EyeDentify-GitHub/`. Website screenshots and the circuit diagram are in the root `docs/` directory. The hosted frontend is maintained separately from this hardware repository.

- `src/eyedentify/`: application, inference, OCR, GPIO, speech, and business logic
- `tests/`: hardware-free automated tests
- `scripts/install_pi.sh`: Raspberry Pi OS dependencies and virtual environment
- `scripts/download_model.py`: pretrained model and label downloader
- `systemd/`: boot service
- `config.example.yaml`: pins, thresholds, timing, and language settings
- `DATASETS.md`: model/data provenance and training notes

## Privacy and accessibility

Frames are processed in memory and are not uploaded or saved. Object detection, OCR, and speech work offline after installation. Bone-conduction audio is recommended so environmental sound remains audible.

## Known limitations

- One forward-facing ultrasonic reading is associated with the selected camera detection; it cannot measure each object's independent depth.
- COCO labels are general-purpose and are not a substitute for mobility-specific hazard recognition.
- Tesseract needs stable framing, adequate light, and readable print.
- Bluetooth pairing and the selected audio profile are managed by Raspberry Pi OS, not this application.

