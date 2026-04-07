# Mini-ADAS: Deep Learning Based Advanced Driver Assistance System

A Python-based Advanced Driver Assistance System (ADAS) that performs real-time forward collision warning and lane detection using deep learning and computer vision techniques.

## Project Overview

This project implements two core ADAS functionalities:
- Forward Collision Warning using YOLOv8 object detection and Time-to-Collision estimation
- Lane Detection using Hough Transform (with U-Net architecture implemented for future use)

The system processes dashcam video footage and provides real-time visual alerts when collision risk is detected.

## Project Structure
mini-ADAS/
│
├── modules/
│   ├── object_detection/
│   │   └── detector.py          # YOLOv8 + ByteTracker detection
│   ├── distance_estimation/
│   │   └── estimator.py         # Monocular distance estimation
│   ├── collision_warning/
│   │   └── ttc_calculator.py    # TTC calculation and risk classification
│   ├── visualization/
│   │   └── display.py           # Frame annotation and warning display
│   └── lane_detection/
│       ├── model.py             # U-Net architecture (PyTorch)
│       ├── preprocess.py        # Dataset preprocessing
│       ├── train.py             # Training loop
│       └── inference.py        # Lane detection inference
│
├── data/
│   ├── raw/
│   │   └── sample_videos/       # Input dashcam footage
│   └── processed/               # Preprocessed data
│
├── models/                      # Saved model weights
├── outputs/                     # Processed video output
├── notebooks/                   # Experimentation notebooks
├── tests/                       # Unit tests
├── main.py                      # Main pipeline entry point
├── config.py                    # Centralized configuration
├── requirements.txt             # Python dependencies
└── README.md
## System Architecture

The pipeline processes each video frame sequentially through the following modules:
Input Frame
|
├── Lane Detection Module    → Lane mask overlay
|
├── Object Detection Module  → Detected vehicles and pedestrians
|        |
├── Distance Estimation      → Distance per detected object (metres)
|        |
├── TTC Calculator           → Time-to-collision and risk level
|
└── Display Module           → Annotated output frame

## Technologies Used

- Python 3.10
- PyTorch 2.5.1 (CUDA 12.1)
- OpenCV 4.13
- Ultralytics YOLOv8
- ByteTracker
- NumPy

## Hardware Requirements

- NVIDIA GPU recommended (tested on RTX 4060 Laptop GPU, 8GB VRAM)
- Minimum 8GB RAM
- Windows 10/11 or Linux

## Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/mini-ADAS.git
cd mini-ADAS
```
2. Create and activate conda environment:
```
conda create -n adas python=3.10
conda activate adas
```
3. Install PyTorch with CUDA support:
```
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```
4. Install remaining dependencies:
```
pip install -r requirements.txt
```
## Configuration

All system parameters are centralized in config.py:

- VIDEO_SOURCE: Path to input video file
- FOCAL_LENGTH: Camera focal length for distance estimation (default: 409)
- KNOWN_VEHICLE_WIDTH: Average vehicle width in metres (default: 1.8)
- TTC_SAFE: Safe TTC threshold in seconds (default: 8.0)
- TTC_CAUTION: Caution TTC threshold in seconds (default: 5.0)
- TTC_HIGH_RISK: High risk TTC threshold in seconds (default: 3.0)
- YOLO_CONFIDENCE: Detection confidence threshold (default: 0.5)

## Running the System

Place your dashcam video in data/raw/sample_videos/ and update VIDEO_SOURCE in config.py, then run:
```
python main.py
```
Press Q to quit.

## Module Descriptions

### Object Detection
Uses YOLOv8n (nano) pretrained on COCO dataset with ByteTracker for multi-object tracking. Detects vehicles (cars, trucks, buses, motorcycles) and pedestrians. Each detection returns a consistent track ID, bounding box coordinates, class label, and confidence score.

### Distance Estimation
Estimates distance to detected objects using the similar triangles method based on known average vehicle width and camera focal length. Distance is calculated as:
Distance = (Known Width x Focal Length) / Pixel Width
Distance measurements are smoothed over 15 frames to reduce bounding box jitter.

### TTC Calculator
Calculates Time-to-Collision using relative speed derived from distance change between frames:
Relative Speed = Distance Change x FPS
TTC = Current Distance / Relative Speed
Risk is classified as SAFE (TTC > 8s), CAUTION (TTC 5-8s), or HIGH RISK (TTC < 3s).

### Lane Detection
Currently implemented using Hough Transform:
- Grayscale conversion and Canny edge detection
- Region of interest masking
- Probabilistic Hough Line Transform
- Lane line filtering by angle

U-Net based deep learning segmentation architecture is implemented in model.py for future training on the TuSimple lane detection dataset.

### Visualization
Draws color-coded bounding boxes (green/yellow/red based on risk), distance and TTC labels with filled backgrounds for readability, lane overlays, and a full-width warning banner when HIGH RISK or CAUTION is detected.

## Limitations

- Distance estimation uses monocular camera geometry which provides approximate results. Real ADAS systems use radar or LiDAR for accurate depth measurement.
- Lane detection via Hough Transform does not handle curved roads reliably. U-Net based segmentation is implemented but requires training on labeled data.
- TTC calculation assumes constant velocity between frames and may be noisy at low frame rates.
- System is designed for forward-facing dashcam footage only.

## Future Improvements

- Train U-Net on TuSimple dataset for robust lane detection
- Fine-tune YOLOv8 on dashcam-specific dataset for improved detection
- Implement proper camera calibration for accurate distance estimation
- Add audio alerts for collision warnings
- Extend to support night driving and adverse weather conditions

## References

1. Redmon et al., "You Only Look Once", CVPR 2016
2. Ronneberger et al., "U-Net: Convolutional Networks for Biomedical Image Segmentation", MICCAI 2015
3. Zhang et al., "ByteTrack: Multi-Object Tracking by Associating Every Detection Box", ECCV 2022
4. McCall and Trivedi, "Video-Based Lane Estimation and Tracking", IEEE ITS 2006

## Author

Prateek Pandey
23FE10CAI00424
Suhani Sharma 
23FE10CAI00220
B.Tech Computer Science and Engineering (AIML)
Manipal University Jaipur