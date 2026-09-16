"""
config.py
---------
Centralized configuration for the Face Detection CLI project.

Keeping all tunable values in one place makes the project easier to
maintain and extend (Maintainability, one of our non-functional
requirements).
"""

import os
import cv2

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
LOG_DIR = os.path.join(BASE_DIR, "logs")

# Haar Cascade file that ships with OpenCV itself (no download needed).
HAAR_CASCADE_PATH = os.path.join(
    cv2.data.haarcascades, "haarcascade_frontalface_default.xml"
)

# DNN model files (must be downloaded separately -- see README.md).
DNN_PROTOTXT_PATH = os.path.join(MODELS_DIR, "deploy.prototxt")
DNN_WEIGHTS_PATH = os.path.join(
    MODELS_DIR, "res10_300x300_ssd_iter_140000.caffemodel"
)

# ---------------------------------------------------------------------------
# Detection parameters
# ---------------------------------------------------------------------------
# Haar Cascade parameters
HAAR_SCALE_FACTOR = 1.1
HAAR_MIN_NEIGHBORS = 5
HAAR_MIN_SIZE = (30, 30)

# DNN parameters
DNN_INPUT_SIZE = (300, 300)
DNN_CONFIDENCE_THRESHOLD = 0.5
DNN_MEAN_VALUES = (104.0, 177.0, 123.0)

# ---------------------------------------------------------------------------
# Drawing / output
# ---------------------------------------------------------------------------
BOX_COLOR = (0, 255, 0)      # BGR - green
BOX_THICKNESS = 2
LABEL_FONT = cv2.FONT_HERSHEY_SIMPLEX
LABEL_FONT_SCALE = 0.5

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
LOG_FILE = os.path.join(LOG_DIR, "face_detection.log")
LOG_LEVEL = "INFO"

# Ensure required directories exist at import time.
for directory in (OUTPUT_DIR, LOG_DIR):
    os.makedirs(directory, exist_ok=True)
