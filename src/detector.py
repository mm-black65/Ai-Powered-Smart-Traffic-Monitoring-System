from ultralytics import YOLO

class TrafficDetector:

    def __init__(self, model_path="../models/yolov8n.pt", confidence_threshold=0.4):
        self.model= YOLO(model_path)
        self.confidence_threshold = confidence_threshold
        self.target_classes = {
        0: "person",
        2: "car",
        3: "motorcycle",
        5: "bus",
        7: "truck",
        9: "traffic light"
        }

    def detect(self, frame):
        results = self.model(frame, conf=self.confidence_threshold, verbose=False)

        detections = []

        for result in results:
            for box in result.boxes:

                class_id = int(box.cls[0])

                if class_id not in self.target_classes:
                   continue

                class_name = self.target_classes[class_id]

                confidence = float(box.conf[0])

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                detections.append({
                    "class_id": class_id,
                    "class_name": class_name,
                    "confidence": confidence,
                    "bbox": (x1, y1, x2, y2)
            })

        return detections