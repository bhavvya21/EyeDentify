from __future__ import annotations

import re


def clean_text(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\s*\n\s*", " ", text)
    return re.sub(r"\s+", " ", text).strip()


class TesseractReader:
    def __init__(self, language: str = "eng"):
        self.language = language

    def read(self, frame) -> str:
        import cv2
        import pytesseract
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.bilateralFilter(gray, 7, 55, 55)
        binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 11)
        return clean_text(pytesseract.image_to_string(binary, lang=self.language, config="--oem 1 --psm 6"))


class SimulatedReader:
    def read(self, _frame) -> str:
        return "Caution: Wet Floor."

