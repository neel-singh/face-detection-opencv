#!/usr/bin/env python3
"""
main.py
-------
Command-line entry point for the Face Detection project.

Usage examples
--------------
Detect faces in a single image:
    python main.py --mode image --input photo.jpg --method haar

Detect faces in a video file:
    python main.py --mode video --input clip.mp4 --method dnn

Detect faces using the webcam (index 0), showing a live preview:
    python main.py --mode webcam --show

Run `python main.py --help` for the full list of options.
"""

import argparse
import sys

from modules.face_detector import create_detector
from modules.image_processor import ImageProcessor
from modules.video_processor import VideoProcessor
from modules.logger_config import get_logger

logger = get_logger("main")


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="face-detection-cli",
        description="Detect faces in images, video files, or a live webcam feed.",
    )
    parser.add_argument(
        "--mode",
        choices=["image", "video", "webcam"],
        required=True,
        help="Input source type.",
    )
    parser.add_argument(
        "--input",
        help="Path to the input image or video file. Not required for --mode webcam.",
    )
    parser.add_argument(
        "--output",
        help="Path to write the annotated output. Auto-generated if omitted.",
    )
    parser.add_argument(
        "--method",
        choices=["haar", "dnn"],
        default="haar",
        help="Face detection backend to use (default: haar).",
    )
    parser.add_argument(
        "--camera-index",
        type=int,
        default=0,
        help="Webcam device index for --mode webcam (default: 0).",
    )
    parser.add_argument(
        "--frame-skip",
        type=int,
        default=1,
        help="Run the detector every N frames for video/webcam (default: 1 = every frame).",
    )
    parser.add_argument(
        "--max-frames",
        type=int,
        default=None,
        help="Stop after this many frames (useful for headless/CI test runs).",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="Display a live preview window (requires a GUI-enabled environment).",
    )
    return parser


def main(argv=None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    if args.mode in ("image", "video") and not args.input:
        parser.error(f"--input is required for --mode {args.mode}")

    try:
        detector = create_detector(args.method)
    except (ValueError, IOError) as exc:
        logger.error("Failed to initialize detector: %s", exc)
        return 1

    try:
        if args.mode == "image":
            processor = ImageProcessor(detector)
            output_path = processor.process(args.input, args.output)
            print(f"Done. Annotated image saved to: {output_path}")

        elif args.mode == "video":
            processor = VideoProcessor(detector, detect_every_n_frames=args.frame_skip)
            output_path = processor.process(
                args.input,
                args.output,
                show_window=args.show,
                max_frames=args.max_frames,
            )
            print(f"Done. Annotated video saved to: {output_path}")

        elif args.mode == "webcam":
            processor = VideoProcessor(detector, detect_every_n_frames=args.frame_skip)
            output_path = processor.process(
                args.camera_index,
                args.output,
                show_window=args.show,
                max_frames=args.max_frames,
            )
            print(f"Done. Annotated recording saved to: {output_path}")

    except (FileNotFoundError, ValueError, IOError) as exc:
        logger.error("Processing failed: %s", exc)
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
