"""
image_processor.py
-------------------
Functional Module 1: Image Input/Output & Processing.

Responsible for everything related to still images: loading a file
from disk, validating it, running a FaceDetector over it, drawing the
results, and saving the annotated output. Keeping this separate from
video handling (module 3) and from detection logic (module 2) is what
gives the project its "clear input/output structure" and modular
design.
"""

import os
import time

import cv2

import config
from modules.face_detector import FaceDetector
from modules.logger_config import get_logger
from modules.utils import annotate_face_count, draw_detections, format_summary

logger = get_logger(__name__)


class ImageProcessor:
    """Loads an image, runs face detection on it, and saves the result."""

    def __init__(self, detector: FaceDetector):
        self._detector = detector

    def process(self, input_path: str, output_path: str = None) -> str:
        """Run face detection on a single image file.

        Returns
        -------
        The path the annotated image was written to.

        Raises
        ------
        FileNotFoundError if `input_path` does not exist.
        ValueError if the file cannot be decoded as an image.
        """
        if not os.path.isfile(input_path):
            raise FileNotFoundError(f"Input image not found: {input_path}")

        frame = cv2.imread(input_path)
        if frame is None:
            raise ValueError(
                f"Could not read '{input_path}' as an image. "
                "Is it a valid JPG/PNG file?"
            )

        start = time.time()
        boxes = self._detector.detect(frame)
        elapsed = time.time() - start

        draw_detections(frame, boxes)
        annotate_face_count(frame, len(boxes))

        if output_path is None:
            base = os.path.splitext(os.path.basename(input_path))[0]
            output_path = os.path.join(config.OUTPUT_DIR, f"{base}_detected.jpg")

        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        cv2.imwrite(output_path, frame)

        logger.info(format_summary(input_path, self._detector.name, len(boxes), elapsed))
        return output_path
