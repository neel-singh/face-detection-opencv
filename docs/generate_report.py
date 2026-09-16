"""
generate_report.py
-------------------
Builds the PDF project report (docs/Project_Report.pdf) required for
portal submission, following the structure specified in the course
instruction document.
"""

import os

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle, ListFlowable, ListItem
)

DOCS_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_PATH = os.path.join(DOCS_DIR, "Project_Report.pdf")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CoverTitle", fontSize=26, leading=32, alignment=TA_CENTER, spaceAfter=20, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="CoverSub", fontSize=14, leading=20, alignment=TA_CENTER, spaceAfter=8))
styles.add(ParagraphStyle(name="H1", fontSize=16, leading=20, spaceBefore=16, spaceAfter=8, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="H2", fontSize=12.5, leading=16, spaceBefore=10, spaceAfter=6, fontName="Helvetica-Bold"))
styles.add(ParagraphStyle(name="Body", fontSize=10.5, leading=15))
styles.add(ParagraphStyle(name="Caption", fontSize=9, leading=12, alignment=TA_CENTER, textColor=colors.grey))

story = []

# ---------------------------------------------------------------------------
# 1. Cover Page
# ---------------------------------------------------------------------------
story.append(Spacer(1, 1.8 * inch))
story.append(Paragraph("Face Detection Using OpenCV", styles["CoverTitle"]))
story.append(Paragraph("A Command-Line Face Detection Tool", styles["CoverSub"]))
story.append(Spacer(1, 0.6 * inch))
story.append(Paragraph("Course: Computer Vision", styles["CoverSub"]))
story.append(Paragraph("Project Report", styles["CoverSub"]))
story.append(Spacer(1, 2.2 * inch))
story.append(Paragraph("Submitted as part of the Flipped Course Evaluation", styles["Caption"]))
story.append(PageBreak())

# ---------------------------------------------------------------------------
# 2. Introduction
# ---------------------------------------------------------------------------
story.append(Paragraph("1. Introduction", styles["H1"]))
story.append(Paragraph(
    "Face detection is one of the foundational tasks in computer vision, underlying "
    "applications ranging from photo organization to security and human-computer "
    "interaction. This project implements a command-line tool that detects human faces "
    "in images, video files, and live webcam streams using OpenCV, offering a choice "
    "between a classical Haar Cascade classifier and a deep-learning based (DNN/SSD) "
    "detector. The tool draws bounding boxes around every detected face and reports a "
    "running face count, saving the annotated result to disk.",
    styles["Body"]))

# ---------------------------------------------------------------------------
# 3. Problem Statement
# ---------------------------------------------------------------------------
story.append(Paragraph("2. Problem Statement", styles["H1"]))
story.append(Paragraph(
    "Manually reviewing images or video footage to locate human faces is slow and "
    "error-prone. There is a need for a lightweight, easy-to-run tool that can "
    "automatically locate faces in an image, a video file, or a live camera feed, "
    "and clearly mark where they were found, without requiring a GUI or a heavy "
    "machine-learning framework.", styles["Body"]))
story.append(Paragraph(
    "<b>Scope:</b> the project detects the presence and location of faces (bounding "
    "boxes only). Face recognition (identifying who a face belongs to), age/emotion "
    "estimation, and training a new detection model from scratch are explicitly out "
    "of scope.", styles["Body"]))
story.append(Paragraph(
    "<b>Target users:</b> students learning computer vision fundamentals, developers "
    "who need a quick scriptable face-detection step for a larger pipeline, and "
    "anyone wanting to batch-annotate photos or videos with face bounding boxes.",
    styles["Body"]))

# ---------------------------------------------------------------------------
# 4. Functional Requirements
# ---------------------------------------------------------------------------
story.append(Paragraph("3. Functional Requirements", styles["H1"]))
func_reqs = [
    "<b>Image Processing Module:</b> load an image file, run face detection on it, "
    "draw bounding boxes and a face count, and save the annotated result.",
    "<b>Video/Webcam Processing Module:</b> read frames from a video file or a live "
    "webcam, run face detection per frame (with configurable frame-skip), and write "
    "an annotated output video.",
    "<b>Face Detection Module:</b> provide a common interface over two interchangeable "
    "detection backends &mdash; a Haar Cascade classifier and a DNN/SSD deep-learning "
    "detector &mdash; selectable via a command-line flag.",
    "<b>CLI Interface:</b> a single entry point (main.py) exposing all three modes "
    "(image / video / webcam) with clear, self-documenting arguments (--help).",
]
story.append(ListFlowable([ListItem(Paragraph(t, styles["Body"])) for t in func_reqs], bulletType="bullet"))

# ---------------------------------------------------------------------------
# 5. Non-Functional Requirements
# ---------------------------------------------------------------------------
story.append(Paragraph("4. Non-Functional Requirements", styles["H1"]))
cell_style = ParagraphStyle(name="TableCell", fontSize=9, leading=12)
header_style = ParagraphStyle(name="TableHeader", fontSize=9.5, leading=12, textColor=colors.white, fontName="Helvetica-Bold")

nfr_rows = [
    ("Requirement", "How it is addressed"),
    ("Performance", "A --frame-skip option lets the detector run every N frames instead of every "
                     "single frame during video/webcam processing, trading accuracy for speed on "
                     "slower machines."),
    ("Usability", "A simple, self-documenting CLI with --help output, sensible defaults (Haar "
                   "method, auto-named outputs), and consistent flags across all three modes."),
    ("Reliability", "Input files, cascade files, and DNN model files are validated before use; the "
                     "tool raises clear, specific errors (FileNotFoundError, ValueError, IOError) "
                     "instead of crashing unpredictably."),
    ("Maintainability", "A modular package layout with a single-responsibility per file, a common "
                         "FaceDetector abstract interface, and one central config.py for every "
                         "tunable value."),
    ("Error Handling Strategy", "All expected failure modes (missing file, unreadable image, missing "
                                 "model weights, bad camera index, unknown detection method) are caught "
                                 "at the CLI boundary and reported to the user with an actionable message."),
    ("Logging / Monitoring", "Every run logs its input source, detection method, face count, and "
                              "elapsed time to both the console and a persistent logs/face_detection.log "
                              "file via a shared logger."),
]
nfr_data = [[Paragraph(r[0], header_style if i == 0 else cell_style),
             Paragraph(r[1], header_style if i == 0 else cell_style)]
            for i, r in enumerate(nfr_rows)]
nfr_table = Table(nfr_data, colWidths=[1.5 * inch, 4.8 * inch])
nfr_table.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c5f8a")),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
    ("LEFTPADDING", (0, 0), (-1, -1), 5),
    ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ("TOPPADDING", (0, 0), (-1, -1), 4),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
]))
story.append(nfr_table)
story.append(PageBreak())

# ---------------------------------------------------------------------------
# 6. System Architecture
# ---------------------------------------------------------------------------
story.append(Paragraph("5. System Architecture", styles["H1"]))
story.append(Paragraph(
    "The system follows a layered, modular architecture. A CLI layer parses user "
    "input and delegates to either the Image Processor or the Video Processor, both "
    "of which depend only on the abstract FaceDetector interface, not on a specific "
    "detection algorithm. This means a new detector (e.g. a future MediaPipe or "
    "MTCNN backend) could be added without touching the processing or CLI layers.",
    styles["Body"]))
story.append(Image(os.path.join(DOCS_DIR, "architecture_diagram.png"), width=6.3 * inch, height=3.7 * inch))
story.append(Paragraph("Figure 1: System Architecture Diagram", styles["Caption"]))
story.append(PageBreak())

# ---------------------------------------------------------------------------
# 7. Design Diagrams
# ---------------------------------------------------------------------------
story.append(Paragraph("6. Design Diagrams", styles["H1"]))

story.append(Paragraph("6.1 Use Case Diagram", styles["H2"]))
story.append(Image(os.path.join(DOCS_DIR, "use_case_diagram.png"), width=5.8 * inch, height=4.2 * inch))
story.append(Paragraph("Figure 2: Use Case Diagram", styles["Caption"]))
story.append(PageBreak())

story.append(Paragraph("6.2 Workflow / Process Flow Diagram", styles["H2"]))
story.append(Image(os.path.join(DOCS_DIR, "workflow_diagram.png"), width=3.4 * inch, height=7.6 * inch))
story.append(Paragraph("Figure 3: Workflow / Process Flow Diagram", styles["Caption"]))
story.append(PageBreak())

story.append(Paragraph("6.3 Sequence Diagram (Image Mode)", styles["H2"]))
story.append(Image(os.path.join(DOCS_DIR, "sequence_diagram.png"), width=6.3 * inch, height=3.7 * inch))
story.append(Paragraph("Figure 4: Sequence Diagram", styles["Caption"]))
story.append(Spacer(1, 0.2 * inch))

story.append(Paragraph("6.4 Class Diagram", styles["H2"]))
story.append(Image(os.path.join(DOCS_DIR, "class_diagram.png"), width=6.3 * inch, height=4.0 * inch))
story.append(Paragraph("Figure 5: Class Diagram", styles["Caption"]))
story.append(PageBreak())

story.append(Paragraph("6.5 Database / Storage Design", styles["H2"]))
story.append(Paragraph(
    "Not applicable. This project does not persist data in a database; it reads "
    "image/video files from disk and writes annotated image/video files back to "
    "disk (see the output/ folder), so no ER diagram or schema is required.",
    styles["Body"]))

# ---------------------------------------------------------------------------
# 8. Design Decisions & Rationale
# ---------------------------------------------------------------------------
story.append(Paragraph("7. Design Decisions & Rationale", styles["H1"]))
decisions = [
    "<b>Abstract FaceDetector base class:</b> chosen so the Image/Video processors "
    "never need to know which algorithm is running underneath &mdash; new detectors "
    "can be plugged in via the create_detector() factory alone.",
    "<b>Haar Cascade as the default backend:</b> it ships inside OpenCV itself, so a "
    "fresh checkout of the project works immediately with zero downloads, which "
    "matters for a course project that must be easy for an evaluator to run.",
    "<b>DNN backend kept optional:</b> the more accurate SSD-based detector needs "
    "external model weight files; rather than bundling large binaries in the Git "
    "repository, the project documents exactly where to download them.",
    "<b>Frame-skip parameter:</b> running a detector on every frame of a video/webcam "
    "stream is the main performance bottleneck; making the skip interval configurable "
    "lets the same code scale from a fast desktop to a slower machine.",
    "<b>Centralized config.py:</b> keeping thresholds, paths, and drawing settings in "
    "one file avoids magic numbers scattered across modules and makes tuning the "
    "detector's sensitivity a one-line change.",
]
story.append(ListFlowable([ListItem(Paragraph(t, styles["Body"])) for t in decisions], bulletType="bullet"))

# ---------------------------------------------------------------------------
# 9. Implementation Details
# ---------------------------------------------------------------------------
story.append(Paragraph("8. Implementation Details", styles["H1"]))
story.append(Paragraph(
    "The project is implemented in Python 3 using OpenCV (cv2) and NumPy. It is "
    "organized into a modules/ package with one file per responsibility:", styles["Body"]))
impl_points = [
    "<b>modules/face_detector.py</b> &ndash; defines the FaceDetector abstract base "
    "class and two implementations: HaarCascadeDetector (cv2.CascadeClassifier) and "
    "DNNFaceDetector (cv2.dnn, Caffe SSD model), plus a create_detector() factory.",
    "<b>modules/image_processor.py</b> &ndash; loads a single image with cv2.imread, "
    "validates it, runs the detector, draws results, and saves the annotated image.",
    "<b>modules/video_processor.py</b> &ndash; wraps cv2.VideoCapture / "
    "cv2.VideoWriter to process a video file or webcam stream frame by frame, "
    "supporting frame-skipping and an optional live preview window.",
    "<b>modules/utils.py</b> &ndash; shared drawing helpers (bounding boxes, face-count "
    "overlay) and a summary-string formatter used for logging.",
    "<b>modules/logger_config.py</b> &ndash; configures one shared logger writing to "
    "both stdout and a rotating log file.",
    "<b>config.py</b> &ndash; all paths, detection thresholds, and drawing constants.",
    "<b>main.py</b> &ndash; argparse-based CLI that wires the above modules together "
    "for the image / video / webcam modes.",
]
story.append(ListFlowable([ListItem(Paragraph(t, styles["Body"])) for t in impl_points], bulletType="bullet"))

# ---------------------------------------------------------------------------
# 10. Screenshots / Results
# ---------------------------------------------------------------------------
story.append(PageBreak())
story.append(Paragraph("9. Screenshots / Results", styles["H1"]))
story.append(Paragraph(
    "Below is an illustrative preview of the tool's annotated output style: green "
    "bounding boxes are drawn around each detected face, labeled 'Face', with a "
    "running total shown in the corner. When run against a real photo or webcam "
    "feed, the same drawing logic (modules/utils.py: draw_detections and "
    "annotate_face_count) produces boxes around the actual detected faces.",
    styles["Body"]))
story.append(Image(os.path.join(DOCS_DIR, "sample_output_preview.png"), width=5.5 * inch, height=3.66 * inch))
story.append(Paragraph("Figure 6: Illustrative annotated-output preview", styles["Caption"]))
story.append(Paragraph(
    "A sample CLI run (Haar Cascade, image mode) on a real photo produces console "
    "output similar to:", styles["Body"]))
story.append(Paragraph(
    "<font face='Courier'>Done. Annotated image saved to: output/photo_detected.jpg</font>",
    styles["Body"]))

# ---------------------------------------------------------------------------
# 11. Testing Approach
# ---------------------------------------------------------------------------
story.append(Paragraph("10. Testing Approach", styles["H1"]))
story.append(Paragraph(
    "Unit tests (tests/test_face_detector.py, tests/test_image_processor.py) use "
    "pytest and synthetically generated images/frames so they run without any "
    "external dataset. They verify:", styles["Body"]))
test_points = [
    "The Haar Cascade classifier loads successfully and reports 0 faces on a blank frame.",
    "The detector factory returns the correct backend and rejects unknown method names "
    "with a ValueError.",
    "Loading a missing image raises FileNotFoundError, and a corrupted/non-image file "
    "raises ValueError, instead of failing silently.",
    "A successful run of ImageProcessor.process() produces a valid, readable output "
    "image file on disk.",
]
story.append(ListFlowable([ListItem(Paragraph(t, styles["Body"])) for t in test_points], bulletType="bullet"))
story.append(Paragraph(
    "In addition, the full CLI (main.py) was manually smoke-tested end-to-end in "
    "image mode to confirm the argument parser, detector, processor, and logger all "
    "integrate correctly.", styles["Body"]))

# ---------------------------------------------------------------------------
# 12. Challenges Faced
# ---------------------------------------------------------------------------
story.append(Paragraph("11. Challenges Faced", styles["H1"]))
challenges = [
    "Balancing detection accuracy against speed for video/webcam input &mdash; solved "
    "with the configurable --frame-skip option rather than a fixed frame rate.",
    "Keeping the DNN backend genuinely optional (since its model files are large "
    "binaries that shouldn't live in Git) while still giving a clear, actionable "
    "error message when someone tries to use --method dnn without downloading them.",
    "Designing a detector interface general enough that Haar Cascade and DNN/SSD "
    "&mdash; two very different underlying algorithms &mdash; can be swapped in "
    "without any change to the calling code.",
]
story.append(ListFlowable([ListItem(Paragraph(t, styles["Body"])) for t in challenges], bulletType="bullet"))

# ---------------------------------------------------------------------------
# 13. Learnings & Key Takeaways
# ---------------------------------------------------------------------------
story.append(Paragraph("12. Learnings & Key Takeaways", styles["H1"]))
story.append(Paragraph(
    "This project reinforced how a clean abstraction (the FaceDetector interface) "
    "pays off immediately even in a small codebase: the image and video pipelines "
    "were written once and never needed to change when a second detection backend "
    "was added. It also highlighted the practical trade-off between classical "
    "computer-vision techniques (Haar Cascades: fast, no training data, weaker on "
    "difficult poses/lighting) and deep-learning detectors (DNN/SSD: more robust, "
    "but heavier and dependent on pre-trained weights).", styles["Body"]))

# ---------------------------------------------------------------------------
# 14. Future Enhancements
# ---------------------------------------------------------------------------
story.append(Paragraph("13. Future Enhancements", styles["H1"]))
future = [
    "Add a third backend using MediaPipe or a modern MTCNN model for better accuracy "
    "on small/occluded faces.",
    "Batch-process an entire folder of images in one command.",
    "Optional face blurring/anonymization mode for privacy-preserving use cases.",
    "Export detection results (bounding boxes, confidence, timestamps) as a "
    "structured CSV/JSON report alongside the annotated media.",
]
story.append(ListFlowable([ListItem(Paragraph(t, styles["Body"])) for t in future], bulletType="bullet"))

# ---------------------------------------------------------------------------
# 15. References
# ---------------------------------------------------------------------------
story.append(Paragraph("14. References", styles["H1"]))
refs = [
    "OpenCV Documentation &ndash; Cascade Classifier: https://docs.opencv.org/",
    "OpenCV DNN Face Detector (SSD/ResNet, Caffe model) &ndash; OpenCV GitHub samples repository.",
    "Viola, P. and Jones, M. (2001). Rapid Object Detection using a Boosted Cascade "
    "of Simple Features.",
    "Python argparse and logging standard library documentation.",
]
story.append(ListFlowable([ListItem(Paragraph(t, styles["Body"])) for t in refs], bulletType="bullet"))

doc = SimpleDocTemplate(
    OUT_PATH, pagesize=A4,
    topMargin=0.8 * inch, bottomMargin=0.8 * inch,
    leftMargin=0.9 * inch, rightMargin=0.9 * inch,
)
doc.build(story)
print("Report written to:", OUT_PATH)
