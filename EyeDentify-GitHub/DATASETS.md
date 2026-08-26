# Models and datasets

EyeDentify performs inference with Google's pretrained COCO EfficientDet-Lite0 TensorFlow Lite Raspberry Pi model. The setup script downloads `detect.tflite` from TensorFlow's public model storage; `labelmap.txt` is included in this repository.

No training dataset is required on the Raspberry Pi. Do not commit the full COCO dataset to GitHub: it is large, unnecessary at runtime, and has its own image licenses. If retraining is required, obtain COCO from <https://cocodataset.org/#download> and review its terms and per-image licenses.

OCR uses Tesseract's packaged English language data (`tesseract-ocr-eng`), installed by `scripts/install_pi.sh`. Add another Debian language package and change `reading.language` in `config.yaml` for other languages.
