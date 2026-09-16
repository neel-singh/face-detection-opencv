"""
video_processor.py
-------------------
Functional Module 3: Video / Webcam Processing.

Handles frame-by-frame face detection for either a webcam feed
(source=0, 1, ...) or a video file on disk, and optionally writes the
annotated result to a new video file.

Frame-skip support (`detect_every_n_frames`) is what satisfies the
"Performance" non-functional requirement: on a slow machine you can
trade detection frequency for smoother playback instead of running
the (expensive) detector on every single frame.
"""

import os
import time

import cv2

import config
from modules.face_detector import FaceDetector
from modules.logger_config import get_logger
from modules.utils import annotate_face_count, draw_detections, format_summary

logger = get_logger(__name__)


class VideoProcessor:
    """Runs face detection over a live webcam feed or a video file."""

    def __init__(self, detector: FaceDetector, detect_every_n_frames: int = 1):
        self._detector = detector
        self._detect_every_n_frames = max(1, detect_every_n_frames)

    def process(
        self,
        source,
        output_path: str = None,
        show_window: bool = False,
        max_frames: int = None,
    ) -> str:
        """Process a video source frame by frame.

        Parameters
        ----------
        source: int (webcam index) or str (path to a video file)
        output_path: where to write the annotated video (auto-named if None)
        show_window: if True, display a live preview window (requires a GUI)
        max_frames: stop after this many frames (useful for CLI/headless runs)

        Returns
        -------
        The path the annotated video was written to.
        """
        cap = cv2.VideoCapture(source)
        if not cap.isOpened():
            raise IOError(f"Could not open video source: {source}")

        fps = cap.get(cv2.CAP_PROP_FPS) or 20.0
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if output_path is None:
            tag = "webcam" if isinstance(source, int) else os.path.splitext(
                os.path.basename(str(source))
            )[0]
            output_path = os.path.join(config.OUTPUT_DIR, f"{tag}_detected.mp4")
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

        frame_index = 0
        last_boxes = []
        start = time.time()

        try:
            while True:
                ok, frame = cap.read()
                if not ok:
                    break

                # Only run the (expensive) detector every N frames; reuse
                # the previous boxes on skipped frames for smoothness.
                if frame_index % self._detect_every_n_frames == 0:
                    last_boxes = self._detector.detect(frame)

                draw_detections(frame, last_boxes)
                annotate_face_count(frame, len(last_boxes))
                writer.write(frame)

                if show_window:
                    cv2.imshow("Face Detection (press 'q' to quit)", frame)
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break

                frame_index += 1
                if max_frames is not None and frame_index >= max_frames:
                    break
        finally:
            cap.release()
            writer.release()
            if show_window:
                cv2.destroyAllWindows()

        elapsed = time.time() - start
        logger.info(
            format_summary(str(source), self._detector.name, len(last_boxes), elapsed)
            + f" | Frames processed: {frame_index}"
        )
        return output_path
