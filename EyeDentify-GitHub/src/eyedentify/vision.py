from __future__ import annotations

import logging
from pathlib import Path
import numpy as np

from .core import Detection

LOG = logging.getLogger(__name__)


class OpenCVCamera:
    def __init__(self, index: int, width: int, height: int):
        import cv2
        self.cv2 = cv2
        self.capture = cv2.VideoCapture(index, cv2.CAP_V4L2)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        if not self.capture.isOpened():
            raise RuntimeError(f"Camera {index} could not be opened")

    def frame(self):
        ok, image = self.capture.read()
        if not ok or image is None:
            raise RuntimeError("Camera frame capture failed")
        return image

    def close(self) -> None:
        self.capture.release()


class TFLiteDetector:
    def __init__(self, model_path: str, labels_path: str, score_threshold: float = 0.55, max_results: int = 5):
        try:
            from tflite_runtime.interpreter import Interpreter
        except ImportError:
            try:
                from ai_edge_litert.interpreter import Interpreter
            except ImportError:
                try:
                    from tensorflow.lite import Interpreter
                except ImportError as exc:
                    raise RuntimeError("No TensorFlow Lite interpreter found; run scripts/install_pi.sh") from exc
        if not Path(model_path).is_file():
            raise FileNotFoundError(f"Model missing: {model_path}. Run scripts/download_model.py")
        self.labels = [line.strip() for line in Path(labels_path).read_text(encoding="utf-8").splitlines() if line.strip()]
        self.threshold, self.max_results = score_threshold, max_results
        self.interpreter = Interpreter(model_path=model_path, num_threads=4)
        self.interpreter.allocate_tensors()
        self.input = self.interpreter.get_input_details()[0]
        self.outputs = self.interpreter.get_output_details()

    def detect(self, bgr_frame) -> list[Detection]:
        import cv2
        height, width = self.input["shape"][1:3]
        rgb = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
        resized = cv2.resize(rgb, (width, height))
        data = np.expand_dims(resized, axis=0)
        if self.input["dtype"] == np.float32:
            data = (data.astype(np.float32) - 127.5) / 127.5
        else:
            data = data.astype(self.input["dtype"])
        self.interpreter.set_tensor(self.input["index"], data)
        self.interpreter.invoke()
        tensors = [np.squeeze(self.interpreter.get_tensor(item["index"])) for item in self.outputs]
        # TensorFlow 1 detection-postprocess models expose boxes, classes, scores, count.
        boxes = next((x for x in tensors if x.ndim == 2 and x.shape[-1] == 4), tensors[0])
        vectors = [x for x in tensors if x.ndim == 1 and len(x) >= len(boxes)]
        scores = next((x for x in vectors if np.all((x >= 0) & (x <= 1)) and np.any(x % 1 != 0)), vectors[-1])
        classes = next((x for x in vectors if x is not scores), vectors[0])
        found = []
        for box, cls, score in zip(boxes, classes, scores):
            if float(score) < self.threshold:
                continue
            ymin, xmin, ymax, xmax = map(float, box)
            class_id = int(cls)
            label = self.labels[class_id] if 0 <= class_id < len(self.labels) else f"object {class_id}"
            found.append(Detection(label, float(score), xmin, ymin, xmax, ymax))
        return sorted(found, key=lambda item: item.score, reverse=True)[: self.max_results]


class SimulatedCamera:
    def frame(self):
        return np.zeros((480, 640, 3), dtype=np.uint8)

    def close(self) -> None:
        pass


class SimulatedDetector:
    def detect(self, _frame) -> list[Detection]:
        return [Detection("person", 0.91, 0.58, 0.1, 0.88, 0.95)]

