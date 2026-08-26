from __future__ import annotations

import shutil
import subprocess


class EspeakSpeaker:
    def __init__(self, rate: int = 175, volume: int = 100):
        self.rate, self.volume = int(rate), int(volume)
        self.binary = shutil.which("espeak-ng") or shutil.which("espeak")
        if not self.binary:
            raise RuntimeError("espeak-ng is not installed")

    def say(self, message: str) -> None:
        subprocess.run([self.binary, "-s", str(self.rate), "-a", str(self.volume), message], check=False, timeout=30)


class ConsoleSpeaker:
    def say(self, message: str) -> None:
        print(f"SPEAK: {message}", flush=True)

