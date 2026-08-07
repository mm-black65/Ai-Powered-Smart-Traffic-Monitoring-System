# 🚦 AI-Powered Smart Traffic Monitoring System Using Computer Vision

An intelligent computer vision system that analyzes prerecorded traffic videos to detect traffic lights, vehicles, pedestrians, and vehicle license plates. The system performs real-time traffic analysis, recognizes traffic signal states, extracts license plate information, and generates an annotated output video with live traffic statistics.

This project demonstrates the integration of deep learning, image processing, and optical character recognition (OCR) for intelligent transportation and smart city applications.

---

## Features

- 🚦 Traffic Light Detection
- 🔴🟡🟢 Traffic Light State Recognition (Red, Yellow, Green)
- 🚗 Vehicle Detection
  - Car
  - Motorcycle
  - Bus
  - Truck
- 🚶 Pedestrian Detection
- 🔢 License Plate Detection
- 📝 License Plate Recognition (OCR)
- 📊 Live Vehicle & Pedestrian Statistics
- 🎥 Annotated Output Video

---

## Technologies Used

- Python
- OpenCV
- Ultralytics YOLO
- PyTorch
- NumPy
- EasyOCR

---

## Project Structure

```
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
│   └── utils.py
│
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/yourusername/AI-Powered-Smart-Traffic-Monitoring.git
cd AI-Powered-Smart-Traffic-Monitoring
```

Create a virtual environment

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

Install the required packages

```bash
pip install -r requirements.txt
```

---

## Usage

Place your traffic video inside the `videos` directory.

Run the application

```bash
python src/main.py
```

The processed video will be saved in the `output` directory.

---

## Applications

- Smart Traffic Monitoring
- Intelligent Transportation Systems (ITS)
- Smart Cities
- Traffic Surveillance
- Road Safety Analysis
- Urban Traffic Analytics

---

## Future Enhancements

- Multi-object tracking
- Vehicle speed estimation
- Lane detection
- Red-light violation detection
- Traffic congestion analysis
- Dashboard for live monitoring
- Real-time webcam support

---

## License

This project is licensed under the MIT License.