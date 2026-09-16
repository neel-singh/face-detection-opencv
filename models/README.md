# DNN Model Files

The `--method dnn` option needs two files placed in this folder:

| File | Purpose |
|---|---|
| `deploy.prototxt` | Network architecture definition |
| `res10_300x300_ssd_iter_140000.caffemodel` | Pre-trained weights |

These are the standard OpenCV "SSD ResNet" face detector files, part of
the official OpenCV GitHub samples. Download them from:

- `deploy.prototxt`:
  https://github.com/opencv/opencv/raw/master/samples/dnn/face_detector/deploy.prototxt
- `res10_300x300_ssd_iter_140000.caffemodel`:
  https://github.com/opencv/opencv_3rdparty/raw/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel

Save both files directly into this `models/` folder, keeping the exact
file names above. They are intentionally excluded from version control
via `.gitignore` because they are large binary files.

If these files are not present, `--method haar` still works fully
without any download, since the Haar Cascade file ships inside
OpenCV itself.
