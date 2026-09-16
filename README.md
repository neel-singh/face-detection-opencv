# Face Detection CLI using OpenCV

A modular command-line computer vision application for detecting human faces in **images, videos, and live webcam feeds** using OpenCV.

The project supports two detection approaches:

- **Haar Cascade** — fast classical computer-vision detector
- **DNN/SSD** — deep-learning based detector for improved detection accuracy

Built as a **Computer Vision course project**.

![Sample Output](docs/Screenshot%202026-09-17%20020622.png.png)

## Features

- Detect faces in JPG/PNG images
- Detect faces frame-by-frame in video files
- Real-time webcam face detection
- Selectable Haar Cascade or DNN/SSD detector
- Configurable webcam device index
- Frame-skipping for better performance on slower systems
- Automatic annotated output generation
- Centralized application logging
- Modular, class-based Python architecture
- Unit tests using synthetic images
- Architecture, workflow, UML and project-report documentation

## Tech Stack

- **Python 3.9+**
- **OpenCV**
- **NumPy**
- **PyTest**

## Project Structure

```text
face-detection-opencv/
├── main.py                     # CLI entry point
├── config.py                   # Application configuration
├── modules/
│   ├── __init__.py
│   ├── face_detector.py        # Haar + DNN face detectors
│   ├── image_processor.py      # Image processing pipeline
│   ├── video_processor.py      # Video/webcam processing
│   ├── logger_config.py        # Logging configuration
│   └── utils.py                # Drawing and helper utilities
├── tests/
│   ├── __init__.py
│   ├── test_face_detector.py
│   └── test_image_processor.py
├── models/
│   └── README.md               # DNN model setup instructions
├── docs/
│   ├── Project_Report.pdf
│   ├── architecture_diagram.png
│   ├── class_diagram.png
│   ├── sequence_diagram.png
│   ├── use_case_diagram.png
│   ├── workflow_diagram.png
│   └── sample_output_preview.png
├── requirements.txt
├── statement.md
├── .gitignore
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/neel-singh/face-detection-opencv.git
cd face-detection-opencv
```

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
py -3.11 -m venv venv
.env\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

> The OpenCV version is pinned because this project uses the `cv2.CascadeClassifier` API required by the Haar detector.

## Usage

Run all commands from the project root.

### Webcam

Start real-time face detection with Haar Cascade:

```bash
python main.py --mode webcam --show --method haar
```

Press **Q** to close the preview.

### Image

```bash
python main.py --mode image --input path/to/photo.jpg --method haar
```

The annotated image is automatically saved in `output/`.

### Video

```bash
python main.py --mode video --input path/to/video.mp4 --method haar
```

### DNN detector

After downloading the required DNN model files:

```bash
python main.py --mode webcam --show --method dnn
```

See [`models/README.md`](models/README.md) for model setup.

### Command-line help

```bash
python main.py --help
```

| Option | Description | Default |
|---|---|---|
| `--mode` | `image`, `video`, or `webcam` | Required |
| `--input` | Input image/video path | Required for image/video |
| `--output` | Output path | Auto-generated |
| `--method` | `haar` or `dnn` | `haar` |
| `--camera-index` | Webcam device index | `0` |
| `--frame-skip` | Detect every Nth frame | `1` |
| `--max-frames` | Stop after N frames | Unlimited |
| `--show` | Display live preview | Off |

## Testing

Run the test suite with:

```bash
pytest tests/ -v
```

The tests use synthetic images and do not require an external dataset.

## Architecture

The application follows a modular pipeline:

```text
Input
  │
  ├── Image
  ├── Video
  └── Webcam
       │
       ▼
Video/Image Processor
       │
       ▼
Face Detector
  ├── Haar Cascade
  └── DNN / SSD
       │
       ▼
Detection Results
       │
       ├── Bounding Boxes
       ├── Annotated Output
       └── Logs
```

Detailed diagrams are available in the [`docs/`](docs/) directory.

## Performance and Reliability

- `--frame-skip` can reduce computation for video/webcam streams.
- Input paths and detector configuration are validated.
- Detection and processing are separated into independent modules.
- Runtime errors are handled at the CLI boundary.
- Logging is centralized for easier debugging and monitoring.

## DNN Models

DNN model weights are intentionally **not committed to GitHub** because they are binary model files and can be large.

Follow [`models/README.md`](models/README.md) to download and place the required files locally.

## Documentation

The repository includes:

- Project report
- System architecture diagram
- Workflow diagram
- Use case diagram
- Class diagram
- Sequence diagram
- Problem statement

See [`docs/Project_Report.pdf`](docs/Project_Report.pdf) for the complete report.

## Author

**Neel Singh**

Computer Science Undergraduate  
Computer Vision Course Project

## License

This project was developed for academic/educational purposes.
