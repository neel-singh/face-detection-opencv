"""
test_image_processor.py
------------------------
Validation tests for modules.image_processor.
"""

import os

import cv2
import numpy as np
import pytest

from modules.face_detector import HaarCascadeDetector
from modules.image_processor import ImageProcessor


@pytest.fixture
def sample_image_path(tmp_path):
    """Create a small synthetic JPEG on disk for the test to use."""
    img = np.full((120, 160, 3), 200, dtype=np.uint8)
    path = tmp_path / "sample.jpg"
    cv2.imwrite(str(path), img)
    return str(path)


def test_process_raises_on_missing_file():
    processor = ImageProcessor(HaarCascadeDetector())
    with pytest.raises(FileNotFoundError):
        processor.process("no_such_file.jpg")


def test_process_writes_annotated_output(sample_image_path, tmp_path):
    processor = ImageProcessor(HaarCascadeDetector())
    output_path = str(tmp_path / "out.jpg")

    result_path = processor.process(sample_image_path, output_path)

    assert result_path == output_path
    assert os.path.isfile(output_path)
    # The annotated image should be a valid, readable image file.
    assert cv2.imread(output_path) is not None


def test_process_rejects_non_image_file(tmp_path):
    bad_file = tmp_path / "not_an_image.jpg"
    bad_file.write_text("this is definitely not image data")

    processor = ImageProcessor(HaarCascadeDetector())
    with pytest.raises(ValueError):
        processor.process(str(bad_file))
