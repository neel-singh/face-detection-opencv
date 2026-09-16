"""
utils.py
--------
Small, reusable helper functions shared across modules: drawing
bounding boxes/labels on frames and formatting summary statistics.
Kept separate from the core logic so each file stays focused on one
responsibility (Maintainability).
"""

from typing import List, Tuple

import cv2

import config

BoundingBox = Tuple[int, int, int, int]


def draw_detections(
    frame,
    boxes: List[BoundingBox],
    label: str = "Face",
):
    """Draw a rectangle + label for every detected face on `frame` in place."""
    for (x, y, w, h) in boxes:
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            config.BOX_COLOR,
            config.BOX_THICKNESS,
        )
        cv2.putText(
            frame,
            label,
            (x, max(0, y - 10)),
            config.LABEL_FONT,
            config.LABEL_FONT_SCALE,
            config.BOX_COLOR,
            1,
            cv2.LINE_AA,
        )
    return frame


def annotate_face_count(frame, count: int):
    """Write the total number of detected faces in the top-left corner."""
    cv2.putText(
        frame,
        f"Faces detected: {count}",
        (10, 25),
        config.LABEL_FONT,
        0.7,
        (255, 255, 255),
        2,
        cv2.LINE_AA,
    )
    return frame


def format_summary(source: str, method: str, face_count: int, elapsed_s: float) -> str:
    """Build a short human-readable summary string for CLI output/logs."""
    return (
        f"Source: {source} | Method: {method} | "
        f"Faces detected: {face_count} | Time: {elapsed_s:.3f}s"
    )
