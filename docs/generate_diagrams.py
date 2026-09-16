"""
generate_diagrams.py
---------------------
One-off helper script that draws the project's design diagrams
(architecture, workflow, use case, class, sequence) with matplotlib
and saves them as PNG files in this docs/ folder.

This is a documentation utility, not part of the runtime application.
Run it with:  python docs/generate_diagrams.py
"""

import os

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

BOX_STYLE = dict(boxstyle="round,pad=0.4", linewidth=1.5)


def box(ax, x, y, w, h, text, facecolor="#dbe9f7", edgecolor="#2c5f8a", fontsize=10):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=BOX_STYLE["boxstyle"],
        linewidth=BOX_STYLE["linewidth"],
        facecolor=facecolor,
        edgecolor=edgecolor,
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fontsize, wrap=True)
    return patch


def arrow(ax, xy_from, xy_to, text=None, style="-|>", color="#333333"):
    a = FancyArrowPatch(
        xy_from, xy_to,
        arrowstyle=style, mutation_scale=15,
        color=color, linewidth=1.4,
    )
    ax.add_patch(a)
    if text:
        mx, my = (xy_from[0] + xy_to[0]) / 2, (xy_from[1] + xy_to[1]) / 2
        ax.text(mx, my + 0.15, text, ha="center", fontsize=8, color=color)


def new_axes(figsize=(11, 7), xlim=(0, 11), ylim=(0, 7)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis("off")
    return fig, ax


# ---------------------------------------------------------------------------
# 1. System Architecture Diagram
# ---------------------------------------------------------------------------
def architecture_diagram():
    fig, ax = new_axes(figsize=(11, 6.5), ylim=(0, 6.5))

    box(ax, 4, 5.3, 3, 0.9, "CLI Interface\n(main.py)", "#ffe6cc", "#b35c00")
    box(ax, 0.3, 3.7, 2.8, 0.9, "Config Manager\n(config.py)", "#e6f2ff", "#2c5f8a")
    box(ax, 4, 3.7, 3, 0.9, "Image Processor\n(modules/image_processor.py)", "#dbe9f7", "#2c5f8a")
    box(ax, 7.7, 3.7, 3, 0.9, "Video Processor\n(modules/video_processor.py)", "#dbe9f7", "#2c5f8a")
    box(ax, 4, 2.1, 3, 0.9, "Face Detector\n(Haar Cascade / DNN)", "#d9f2d9", "#2e7d32")
    box(ax, 0.3, 2.1, 2.8, 0.9, "Logger\n(modules/logger_config.py)", "#f2e6ff", "#6a1b9a")
    box(ax, 4, 0.5, 3, 0.9, "Output\n(annotated image / video + logs)", "#fff2cc", "#997a00")

    arrow(ax, (5.5, 5.3), (5.5, 4.6))
    arrow(ax, (1.7, 4.6), (1.7, 5.3))
    arrow(ax, (1.7, 4.6), (4, 4.1))
    arrow(ax, (5.5, 3.7), (5.5, 3.0))
    arrow(ax, (9.2, 3.7), (5.9, 2.7))
    arrow(ax, (5.5, 2.1), (5.5, 1.4))
    arrow(ax, (1.7, 3.7), (4, 4.1))
    arrow(ax, (1.7, 2.5), (4, 2.5))

    ax.set_title("System Architecture Diagram - Face Detection CLI", fontsize=13, fontweight="bold")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "architecture_diagram.png"), dpi=160)
    plt.close(fig)


# ---------------------------------------------------------------------------
# 2. Workflow / Process Flow Diagram
# ---------------------------------------------------------------------------
def workflow_diagram():
    fig, ax = new_axes(figsize=(4.5, 10), xlim=(0, 4.5), ylim=(0, 10))

    steps = [
        "Start",
        "Parse CLI arguments\n(--mode, --input, --method)",
        "Load configuration\n& initialize logger",
        "Create detector\n(Haar Cascade or DNN)",
        "Read input\n(image / video / webcam)",
        "Detect faces\nin frame(s)",
        "Draw bounding boxes\n+ face count",
        "Save annotated\noutput to disk",
        "Log summary",
        "End",
    ]
    y = 9.3
    positions = []
    for i, step in enumerate(steps):
        shape_color = "#d9f2d9" if step in ("Start", "End") else "#dbe9f7"
        edge_color = "#2e7d32" if step in ("Start", "End") else "#2c5f8a"
        box(ax, 0.6, y - 0.55, 3.3, 0.75, step, shape_color, edge_color, fontsize=9)
        positions.append(y - 0.55 + 0.375)
        y -= 1.0

    for i in range(len(positions) - 1):
        arrow(ax, (2.25, positions[i] - 0.375), (2.25, positions[i + 1] + 0.375))

    ax.set_title("Workflow / Process Flow", fontsize=12, fontweight="bold")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "workflow_diagram.png"), dpi=160)
    plt.close(fig)


# ---------------------------------------------------------------------------
# 3. Use Case Diagram
# ---------------------------------------------------------------------------
def use_case_diagram():
    fig, ax = new_axes(figsize=(9, 6.5), xlim=(0, 9), ylim=(0, 6.5))

    # Actor (simple stick figure)
    ax.plot([1.2], [5.0], marker="o", markersize=18, color="#333333")
    ax.add_line(Line2D([1.2, 1.2], [4.55, 3.4], color="#333333", linewidth=2))
    ax.add_line(Line2D([0.6, 1.8], [4.1, 4.1], color="#333333", linewidth=2))
    ax.add_line(Line2D([1.2, 0.6], [3.4, 2.7], color="#333333", linewidth=2))
    ax.add_line(Line2D([1.2, 1.8], [3.4, 2.7], color="#333333", linewidth=2))
    ax.text(1.2, 2.3, "User", ha="center", fontsize=10, fontweight="bold")

    use_cases = [
        ("Detect faces in an image", 3.2, 5.4),
        ("Detect faces in a video file", 3.2, 4.3),
        ("Detect faces via live webcam", 3.2, 3.2),
        ("Select detection method\n(Haar / DNN)", 3.2, 2.1),
        ("Save annotated output", 3.2, 1.0),
    ]
    for text, x, y in use_cases:
        ellipse = plt.matplotlib.patches.Ellipse(
            (x + 2.3, y), 4.6, 0.9, facecolor="#dbe9f7", edgecolor="#2c5f8a", linewidth=1.5
        )
        ax.add_patch(ellipse)
        ax.text(x + 2.3, y, text, ha="center", va="center", fontsize=9)
        arrow(ax, (1.9, 5.0 - (5.4 - y) * 0 if False else 3.8), (x, y), style="-")

    ax.set_title("Use Case Diagram - Face Detection CLI", fontsize=12, fontweight="bold")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "use_case_diagram.png"), dpi=160)
    plt.close(fig)


# ---------------------------------------------------------------------------
# 4. Class Diagram
# ---------------------------------------------------------------------------
def class_diagram():
    fig, ax = new_axes(figsize=(11, 7), xlim=(0, 11), ylim=(0, 7))

    box(ax, 4, 5.6, 3, 1.0,
        "<<abstract>>\nFaceDetector\n--\n+ detect(frame): List[BBox]\n+ name: str",
        "#f2e6ff", "#6a1b9a", fontsize=8.5)

    box(ax, 1, 3.8, 3.2, 1.1,
        "HaarCascadeDetector\n--\n- classifier\n--\n+ detect(frame)",
        "#dbe9f7", "#2c5f8a", fontsize=8.5)
    box(ax, 6.8, 3.8, 3.2, 1.1,
        "DNNFaceDetector\n--\n- net\n- confidence_threshold\n--\n+ detect(frame)",
        "#dbe9f7", "#2c5f8a", fontsize=8.5)

    box(ax, 0.3, 1.6, 3.2, 1.1,
        "ImageProcessor\n--\n- detector\n--\n+ process(path)",
        "#d9f2d9", "#2e7d32", fontsize=8.5)
    box(ax, 4, 1.6, 3.2, 1.1,
        "VideoProcessor\n--\n- detector\n- detect_every_n_frames\n--\n+ process(source)",
        "#d9f2d9", "#2e7d32", fontsize=8.5)
    box(ax, 7.7, 1.6, 3, 1.1,
        "CLI App\n(main.py)\n--\n+ build_arg_parser()\n+ main()",
        "#ffe6cc", "#b35c00", fontsize=8.5)

    # inheritance arrows (open triangle look approximated with normal arrow)
    arrow(ax, (2.6, 4.9), (5.0, 5.6), style="-|>")
    arrow(ax, (8.4, 4.9), (6.0, 5.6), style="-|>")
    # composition/uses arrows
    arrow(ax, (1.9, 2.7), (2.6, 3.8), style="-|>")
    arrow(ax, (5.6, 2.7), (5.6, 3.8), style="-|>")
    arrow(ax, (9.2, 2.7), (9.2, 3.8), style="-|>")

    ax.set_title("Class Diagram - Face Detection CLI", fontsize=12, fontweight="bold")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "class_diagram.png"), dpi=160)
    plt.close(fig)


# ---------------------------------------------------------------------------
# 5. Sequence Diagram (image mode)
# ---------------------------------------------------------------------------
def sequence_diagram():
    fig, ax = new_axes(figsize=(11, 6.5), xlim=(0, 11), ylim=(0, 6.5))

    lifelines = ["User", "CLI (main.py)", "ImageProcessor", "FaceDetector", "Output/Disk"]
    xs = [0.8, 3.0, 5.5, 8.0, 10.0]
    for text, x in zip(lifelines, xs):
        box(ax, x - 0.9, 5.7, 1.8, 0.6, text, "#e6f2ff", "#2c5f8a", fontsize=8.5)
        ax.add_line(Line2D([x, x], [0.3, 5.7], color="#999999", linestyle="--", linewidth=1))

    messages = [
        (0, 1, 5.0, "run: python main.py --mode image ..."),
        (1, 2, 4.4, "process(input_path)"),
        (2, 3, 3.8, "detect(frame)"),
        (3, 2, 3.2, "return bounding boxes"),
        (2, 4, 2.6, "imwrite(annotated frame)"),
        (2, 1, 2.0, "return output_path"),
        (1, 0, 1.4, "print summary"),
    ]
    for src, dst, y, label in messages:
        arrow(ax, (xs[src], y), (xs[dst], y), text=label)

    ax.set_title("Sequence Diagram - Face Detection in Image Mode", fontsize=12, fontweight="bold")
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "sequence_diagram.png"), dpi=160)
    plt.close(fig)


if __name__ == "__main__":
    architecture_diagram()
    workflow_diagram()
    use_case_diagram()
    class_diagram()
    sequence_diagram()
    print("All diagrams generated in:", OUT_DIR)
