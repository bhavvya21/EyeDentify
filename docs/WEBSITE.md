# Eyedentify companion website

[Open the workspace](https://eyedentify-senseai.me-ed0430495.chatgpt.site).

The frontend source is in [`../website/`](../website/), with [PowerShell instructions](../website/README.md). Updating GitHub does not automatically republish the live Sites deployment.

## Current interface

The site contains Overview, Eyedentify dashboard, Reading studio, Sessions and Preferences. Device setup has been removed. The dashboard leaves observations empty when a data source is unavailable; it does not populate readings automatically.

## Browser features

- Enable camera requests permission and displays a local video preview. Leaving its page stops the camera tracks. The app does not capture, save or upload frames.
- Reading studio accepts pasted text and UTF-8 text files up to 200 KB, and requests browser text-to-speech. It prefers an installed local English voice; available voices and any provider processing depend on the browser. It does not store reading text.
- Preferences persist in localStorage on the current browser. Session history has no live producer connected yet.

## Hardware boundary

Raspberry Pi object detection, Tesseract OCR, ultrasonic distance and offline `espeak-ng` speech are separate from the hosted frontend. A secure transport and authenticated device identity are needed before Pi observations can populate the dashboard. The current website does not remotely control GPIO or send camera frames to a model.

Environmental sound classification and movement sensing are not implemented by this web UI. No microphone is activated and no IMU is assumed to be installed. The circuit diagram documents the existing Pi 5, camera, HC-SR04, slide switch and audio configuration only.

## Documentation images

The screenshots were supplied by the project owner and show a previous visual revision that still includes Device setup. They are retained unchanged. The circuit diagram is a separate wiring reference and is not added to the website UI.
