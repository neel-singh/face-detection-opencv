"""
face_detector.py
-----------------
Functional Module 2: Face Detection.

Defines a common FaceDetector interface with two concrete
implementations:

    * HaarCascadeDetector - fast, classical, ships with OpenCV.
    * DNNFaceDetector      - more accurate deep-learning based detector
                              (Caffe SSD model), used when the model
                              files are available.

Using an abstract base class + a factory function
(``create_detector``) means new detection backends can be added later
without changing any calling code - this is what satisfies the
"Scalability" / "Maintainability" non-functional requirements.
"""

from abc import ABC, abstractmethod
from typing import List, Tuple

import cv2
import numpy as np

import config
from modules.logger_config import get_logger

logger = get_logger(__name__)

# A detected face is represented as (x, y, w, h) in pixel coordinates.
BoundingBox = Tuple[int, int, int, int]


class FaceDetector(ABC):
    """Abstract base class every concrete face detector must implement."""

    @abstractmethod
    def detect(self, frame: np.ndarray) -> List[BoundingBox]:
        """Return a list of (x, y, w, h) bounding boxes for detected faces."""
        raise NotImplementedError

    @property
    @abstractmethod
    def name(self) -> str:
        """Human readable name of this detector, used in logs/labels."""
        raise NotImplementedError


class HaarCascadeDetector(FaceDetector):
    """Classical Viola-Jones face detector using OpenCV's Haar Cascades."""

    def __init__(self, cascade_path: str = config.HAAR_CASCADE_PATH):
        self._classifier = cv2.CascadeClassifier(cascade_path)
        if self._classifier.empty():
            # Fail loudly and clearly rather than silently returning
            # zero detections forever (Error handling strategy).
            raise IOError(
                f"Could not load Haar Cascade file at '{cascade_path}'. "
                "Please verify your OpenCV installation."
            )
        logger.info("Loaded Haar Cascade classifier from %s", cascade_path)

    def detect(self, frame: np.ndarray) -> List[BoundingBox]:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)  # improves detection in low light

        faces = self._classifier.detectMultiScale(
            gray,
            scaleFactor=config.HAAR_SCALE_FACTOR,
            minNeighbors=config.HAAR_MIN_NEIGHBORS,
            minSize=config.HAAR_MIN_SIZE,
        )
        return [tuple(map(int, face)) for face in faces]

    @property
    def name(self) -> str:
        return "Haar Cascade"


class DNNFaceDetector(FaceDetector):
    """Deep-learning face detector (ResNet-SSD, Caffe model)."""

    def __init__(
        self,
        prototxt_path: str = config.DNN_PROTOTXT_PATH,
        weights_path: str = config.DNN_WEIGHTS_PATH,
        confidence_threshold: float = config.DNN_CONFIDENCE_THRESHOLD,
    ):
        try:
            self._net = cv2.dnn.readNetFromCaffe(prototxt_path, weights_path)
        except cv2.error as exc:
            raise IOError(
                "Could not load DNN model files. Make sure "
                f"'{prototxt_path}' and '{weights_path}' exist. "
                "See README.md for download instructions."
            ) from exc

        self._confidence_threshold = confidence_threshold
        logger.info("Loaded DNN face detector (weights=%s)", weights_path)

    def detect(self, frame: np.ndarray) -> List[BoundingBox]:
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(
            cv2.resize(frame, config.DNN_INPUT_SIZE),
            1.0,
            config.DNN_INPUT_SIZE,
            config.DNN_MEAN_VALUES,
        )
        self._net.setInput(blob)
        detections = self._net.forward()

        boxes: List[BoundingBox] = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence < self._confidence_threshold:
                continue

            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x1, y1, x2, y2) = box.astype(int)
            # Clip to frame bounds to avoid negative / out-of-range boxes.
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)
            boxes.append((x1, y1, x2 - x1, y2 - y1))

        return boxes

    @property
    def name(self) -> str:
        return "DNN (SSD ResNet)"


def create_detector(method: str = "haar") -> FaceDetector:
    """Factory function: builds the requested detector by name.

    Parameters
    ----------
    method: "haar" or "dnn"

    Raises
    ------
    ValueError if an unknown method name is given.
    """
    method = method.lower().strip()
    if method == "haar":
        return HaarCascadeDetector()
    if method == "dnn":
        return DNNFaceDetector()
    raise ValueError(f"Unknown detection method '{method}'. Use 'haar' or 'dnn'.")
