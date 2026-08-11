# 🚦 AI-Powered Smart Traffic Monitoring System

> **An end-to-end computer vision pipeline for automated traffic scene understanding, vehicle analytics, traffic-light state recognition, and license-plate recognition from prerecorded road footage.**

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-green?logo=opencv)
![YOLO](https://img.shields.io/badge/YOLO-Ultralytics-purple)
![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-red?logo=pytorch)
![EasyOCR](https://img.shields.io/badge/EasyOCR-OCR-orange)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

---
## 🎥 Demo / Output
<p align="center">
  <img src="output\image.png" alt="Smart Traffic Monitoring System Output" width="900">
</p>

---
## 📌 Overview

The **AI-Powered Smart Traffic Monitoring System** is a computer vision pipeline designed to analyze prerecorded traffic footage and automatically extract meaningful information from road scenes.

Instead of manually inspecting traffic videos, the system processes each frame through a sequence of detection, recognition, and analytics modules to identify road users and traffic conditions.

The system currently supports:

* 🚦 Traffic light detection and state recognition
* 🚗 Vehicle detection and classification
* 🚶 Pedestrian detection
* 🔢 License plate detection
* 📝 License plate recognition using OCR
* 📊 Vehicle and pedestrian statistics
* 🎥 Annotated output video generation

The project demonstrates how **deep learning models, image processing, object detection, OCR, and video analytics** can be integrated into a single computer vision application.

---

# 🎯 Problem Statement

Traditional traffic monitoring relies heavily on manual observation or infrastructure-specific sensors.

A vision-based monitoring system can instead use existing video footage to automatically answer questions such as:

* How many vehicles are present?
* What types of vehicles are on the road?
* How many pedestrians are visible?
* What is the current traffic signal state?
* Can visible license plates be extracted?
* How does traffic change throughout the video?

The goal of this project is to build a modular pipeline capable of extracting these observations automatically from traffic footage.

---

# 🧠 System Architecture

The application follows a modular computer vision pipeline:

```text
                 ┌─────────────────────┐
                 │   Traffic Video     │
                 │     (.mp4)          │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Video Processing  │
                 │     / Frame I/O     │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │   Object Detection  │
                 │       YOLO          │
                 └──────────┬──────────┘
                            │
            ┌───────────────┼────────────────┐
            │               │                │
            ▼               ▼                ▼
       🚗 Vehicles      🚶 Pedestrians    🚦 Traffic Light
            │               │                │
            ▼               │                ▼
      Vehicle Counts        │          State Recognition
            │               │
            └───────┬───────┘
                    │
                    ▼
             🔢 License Plates
                    │
                    ▼
              📝 OCR Processing
                    │
                    ▼
             📊 Traffic Analytics
                    │
                    ▼
            🎥 Annotated Video
```

---

# ⚙️ Core Pipeline

## 1. Video Input

The system accepts prerecorded traffic footage as its input.

Each video is read frame-by-frame using OpenCV.

```text
Input Video
     ↓
Frame Extraction
     ↓
Frame Processing
     ↓
Detection & Recognition
     ↓
Annotated Frame
     ↓
Output Video
```

This makes the pipeline deterministic and allows the same footage to be repeatedly tested while developing and evaluating individual modules.

---

## 2. Object Detection

The primary detection stage uses **Ultralytics YOLO** to identify objects within each frame.

The system focuses on traffic-relevant classes:

| Category          | Objects                     |
| ----------------- | --------------------------- |
| 🚗 Vehicles       | Car, Motorcycle, Bus, Truck |
| 🚶 People         | Pedestrian                  |
| 🚦 Infrastructure | Traffic Light               |

For every detected object, the pipeline obtains information such as:

* Class
* Confidence score
* Bounding-box coordinates

Conceptually:

```text
Frame
  │
  ▼
YOLO Detector
  │
  ├── Bounding Box
  ├── Class
  └── Confidence
```

These detections are then passed to downstream modules.

---

# 🚦 Traffic Light Recognition

Traffic-light processing is separated from general object detection.

After identifying a traffic-light region, the system analyzes the corresponding image region to determine the active signal state:

```text
Traffic Light
      │
      ▼
Region of Interest
      │
      ▼
Image Processing
      │
      ├── 🔴 Red
      ├── 🟡 Yellow
      └── 🟢 Green
```

Separating traffic-light recognition from general object detection keeps the system modular and makes it possible to improve the recognition algorithm independently.

---

# 🚗 Vehicle Analytics

The system classifies detected road vehicles into multiple categories:

* Car
* Motorcycle
* Bus
* Truck

The detected objects are aggregated to generate traffic statistics.

Example:

```text
Traffic Statistics

Cars        : 24
Motorcycles : 11
Buses       : 3
Trucks      : 5
Pedestrians : 8
```

These statistics are updated during video processing and can be displayed directly on the annotated frames.

---

# 🚶 Pedestrian Detection

Pedestrians are detected as independent objects rather than being treated as part of vehicle traffic.

This allows the system to maintain separate statistics for:

* Vehicle traffic
* Pedestrian activity

This distinction is useful for future extensions such as pedestrian-density analysis and road-safety monitoring.

---

# 🔢 License Plate Detection

License plate recognition is implemented as a two-stage process.

### Stage 1 — Plate Detection

A dedicated license-plate detection model identifies the plate region.

```text
Vehicle
   │
   ▼
License Plate Detector
   │
   ▼
Plate Bounding Box
```

### Stage 2 — OCR

The detected plate region is then passed to an OCR engine.

```text
Plate Region
     │
     ▼
Preprocessing
     │
     ▼
EasyOCR
     │
     ▼
Recognized Text
```

This separation is important because **detecting a license plate and reading its characters are two different computer vision problems**.

---

# 📊 Traffic Analytics

The analytics module aggregates detections generated throughout the video.

Current metrics include:

* Vehicle counts
* Vehicle-class distribution
* Pedestrian counts
* Traffic-light state

The analytics layer is intentionally separated from the detection layer so that additional metrics can be added without modifying the underlying detection logic.

---

# 🎥 Output Generation

After processing, the system generates an annotated video.

The output contains visual information such as:

```text
┌──────────────────────────────────────────────┐
│ 🚦 Traffic Light: GREEN                     │
│                                              │
│ Cars: 24   Bikes: 11   Bus: 3   Truck: 5   │
│ Pedestrians: 8                              │
│                                              │
│       ┌─────────────┐                       │
│       │     CAR     │                       │
│       │   0.91      │                       │
│       └─────────────┘                       │
│                                              │
│            Traffic Scene                    │
└──────────────────────────────────────────────┘
```

The processed footage is stored in the `output/` directory.

---

# 🏗️ Project Structure

```text
AI-Powered-Smart-Traffic-Monitoring/
│
├── models/
│   ├── yolov8n.pt
│   └── license_plate.pt
│
├── videos/
│   ├── input.mp4
│   └── test.mp4
│
├── output/
│
├── src/
│   ├── main.py
│   ├── detector.py
│   ├── traffic_light.py
│   ├── plate_detector.py
│   ├── ocr.py
│   ├── analytics.py
│   └── tracker.py
│
├── requirements.txt
└── README.md
```

### Module Responsibilities

| Module              | Responsibility                                     |
| ------------------- | -------------------------------------------------- |
| `main.py`           | Application entry point and pipeline orchestration |
| `detector.py`       | General object detection                           |
| `traffic_light.py`  | Traffic-light state recognition                    |
| `plate_detector.py` | License-plate detection                            |
| `ocr.py`            | License-plate text recognition                     |
| `analytics.py`      | Traffic statistics and aggregation                 |
| `tracker.py`        | Object tracking functionality                      |
| `models/`           | Trained/pretrained model weights                   |
| `videos/`           | Input traffic footage                              |
| `output/`           | Generated annotated videos                         |

The modular structure allows individual components to be developed and tested independently rather than placing the entire application inside a single script.

---

# 🛠️ Technology Stack

### Programming

**Python**

Used as the primary development language for integrating the computer vision and deep-learning components.

### Computer Vision

**OpenCV**

Used for:

* Video input/output
* Frame processing
* Image manipulation
* Drawing annotations
* Region-of-interest processing

### Object Detection

**Ultralytics YOLO**

Used for real-time object detection and traffic-object classification.

### Deep Learning

**PyTorch**

Provides the underlying deep-learning framework used by the detection models.

### Optical Character Recognition

**EasyOCR**

Used to extract text from detected license-plate regions.

### Numerical Processing

**NumPy**

Used for numerical operations and image-array manipulation.

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/yourusername/AI-Powered-Smart-Traffic-Monitoring.git

cd AI-Powered-Smart-Traffic-Monitoring
```

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the System

Place the traffic footage inside:

```text
videos/
```

Then run:

```bash
python src/main.py
```

The processed video will be generated inside:

```text
output/
```

---

# 📈 Example Output

The system produces an annotated traffic video containing:

* Bounding boxes around detected objects
* Object class labels
* Detection confidence
* Traffic-light state
* Vehicle statistics
* Pedestrian statistics
* Detected license-plate information

This converts raw traffic footage into a machine-readable and visually interpretable traffic-analysis output.

---

# 🧩 Engineering Design

A key design decision in this project is **separation of responsibilities**.

Instead of implementing all functionality inside one large processing loop, the application separates:

```text
Detection
   ↓
Recognition
   ↓
Tracking
   ↓
Analytics
   ↓
Visualization
```

This provides several advantages:

### Modularity

Individual components can be replaced without redesigning the entire application.

### Maintainability

Each module has a specific responsibility, making the codebase easier to understand and debug.

### Extensibility

New capabilities such as speed estimation or red-light violation detection can be added as independent processing stages.

### Reusability

The same detection and analytics modules can potentially be reused with different traffic datasets or video sources.

---

# 🔬 Current Limitations

The current implementation is designed primarily as a **video-analysis prototype**, and therefore has several limitations:

* Accuracy depends on video quality and camera angle.
* License-plate recognition can degrade with motion blur, small plates, or occlusion.
* Traffic-light recognition depends on visibility and illumination conditions.
* Vehicle counts based solely on frame detections can count the same vehicle multiple times without robust tracking.
* The current system processes prerecorded video rather than a live camera stream.

These limitations provide clear directions for future engineering improvements.

---

# 🔮 Future Development

The architecture is designed to support several advanced traffic-intelligence features.

### 1. Multi-Object Tracking

Assign persistent IDs to detected vehicles and pedestrians.

```text
Detection
    ↓
Tracking
    ↓
Vehicle ID
    ↓
Trajectory
```

This would enable more reliable counting and movement analysis.

### 2. Vehicle Speed Estimation

Estimate vehicle speed using tracked trajectories and calibrated scene geometry.

### 3. Lane Detection

Identify road lanes and determine which lane each vehicle occupies.

### 4. Red-Light Violation Detection

Combine:

```text
Traffic Light State
        +
Vehicle Tracking
        +
Stop Line
        ↓
Violation Detection
```

to automatically identify vehicles crossing during a red signal.

### 5. Traffic Congestion Analysis

Use vehicle density, movement, and lane occupancy to estimate congestion levels.

### 6. Live Monitoring Dashboard

Build a dashboard for displaying:

* Current traffic volume
* Vehicle distribution
* Pedestrian activity
* Signal state
* Detected violations
* Historical statistics

### 7. Real-Time Camera Input

Extend the pipeline from prerecorded footage to live CCTV or webcam streams.

---

# 🌆 Potential Applications

The system can serve as a foundation for:

* Smart-city traffic monitoring
* Intelligent Transportation Systems (ITS)
* Automated traffic surveillance
* Road-safety analysis
* Vehicle-flow analysis
* Traffic congestion monitoring
* License-plate-based traffic studies
* Automated intersection monitoring

---

# 📚 What This Project Demonstrates

This project brings together multiple areas of engineering and AI:

```text
Python
  │
  ├── Computer Vision
  │
  ├── Deep Learning
  │
  ├── Object Detection
  │
  ├── Image Processing
  │
  ├── OCR
  │
  ├── Video Processing
  │
  └── Data Analytics
```

More importantly, it demonstrates the integration of these components into a **single end-to-end computer vision pipeline** rather than using an isolated machine-learning model.

---

# 👨‍💻 Project Status

**Current Status:** 🚧 Active Development

### Implemented

* [x] Video input pipeline
* [x] YOLO-based object detection
* [x] Vehicle classification
* [x] Pedestrian detection
* [x] Traffic-light detection
* [x] Traffic-light state recognition
* [x] License-plate detection
* [x] OCR pipeline
* [x] Traffic statistics
* [x] Annotated video generation

### Planned

* [ ] Robust multi-object tracking
* [ ] Vehicle speed estimation
* [ ] Lane detection
* [ ] Red-light violation detection
* [ ] Congestion estimation
* [ ] Traffic analytics dashboard
* [ ] Real-time camera support

---

# 📄 License

This project is licensed under the **MIT License**.

---

## ⭐ Acknowledgements

This project uses open-source technologies including **Ultralytics YOLO, OpenCV, PyTorch, EasyOCR, and NumPy**.

---

## 📬 Author

**Mahi**

Computer Vision • Robotics • Embedded Systems

```
Built to explore how AI can transform raw traffic
video into actionable transportation intelligence.
```
