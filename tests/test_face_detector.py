"""
test_face_detector.py
----------------------
Validation tests for modules.face_detector.

These do not require any external test images: they check that the
detector loads correctly, behaves sensibly on trivial input (a blank
frame should have zero faces), and that invalid input / configuration
is rejected the way the error-handling strategy promises in the
project report.
"""

import numpy as np
import pytest

from modules.face_detector import HaarCascadeDetector, create_detector


def test_haar_detector_loads_successfully():
    detector = HaarCascadeDetector()
    assert detector.name == "Haar Cascade"


def test_haar_detector_returns_no_faces_on_blank_frame():
    detector = HaarCascadeDetector()
    blank_frame = np.zeros((200, 200, 3), dtype=np.uint8)
    boxes = detector.detect(blank_frame)
    assert boxes == []


def test_create_detector_factory_returns_haar_by_default():
    detector = create_detector("haar")
    assert detector.name == "Haar Cascade"


def test_create_detector_factory_rejects_unknown_method():
    with pytest.raises(ValueError):
        create_detector("not-a-real-method")


def test_haar_detector_bad_cascade_path_raises_ioerror():
    with pytest.raises(IOError):
        HaarCascadeDetector(cascade_path="does/not/exist.xml")
