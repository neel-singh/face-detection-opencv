# Problem Statement

## Problem Statement

Manually reviewing images or video footage to locate human faces is
slow and error-prone, whether the task is organizing a photo
collection, building a simple attendance/monitoring aid, or
pre-processing frames for a downstream computer vision pipeline (e.g.
recognition or emotion analysis). There is a need for a lightweight,
dependency-light tool that can automatically locate faces in an
image, a video file, or a live camera feed, and clearly mark where
they were found.

## Scope of the Project

This project delivers a **command-line face detection tool** built on
OpenCV. It is scoped to:

- Accept a single image, a video file, or a live webcam stream as
  input.
- Detect all human faces present using either a classical Haar
  Cascade classifier or a deep-learning (DNN/SSD) detector, selectable
  by the user.
- Draw bounding boxes and a running face count on the output, and
  save the annotated result to disk.
- Run entirely from the terminal (no GUI required, aside from an
  optional live-preview window).

Out of scope: face *recognition* (identifying *who* a face belongs
to), age/emotion estimation, and training a custom detection model
from scratch — the project uses existing, well-established detection
techniques rather than training new ones.

## Target Users

- Students and hobbyists learning the fundamentals of computer vision.
- Developers who need a quick, scriptable face-detection utility to
  drop into a larger pipeline (e.g. as a pre-processing step before
  face recognition or anonymization).
- Anyone who wants to batch-annotate photos/videos with face
  bounding boxes without writing OpenCV code themselves.

## High-Level Features

1. **Image mode** – detect and annotate faces in a single image file.
2. **Video mode** – detect and annotate faces frame-by-frame in a
   video file, writing an annotated copy.
3. **Webcam mode** – run detection live on a connected camera, with
   an optional on-screen preview.
4. **Selectable detection backend** – Haar Cascade (fast, zero
   setup) or DNN/SSD (more accurate, optional model download).
5. **Configurable performance** – skip frames during video/webcam
   processing to trade accuracy for speed.
6. **Centralized logging** of every run (source, method, faces found,
   processing time) to both console and a log file.
