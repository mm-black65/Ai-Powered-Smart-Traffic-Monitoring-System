from ultralytics import YOLO


class LicensePlateDetector:

    def __init__(
        self,
        model_path="../models/license_plate_detector.pt",
        confidence_threshold=0.35
    ):
        self.model = YOLO(model_path)
        self.confidence_threshold = confidence_threshold

    def detect(self, frame):

        results = self.model(
            frame,
            conf=self.confidence_threshold,
            verbose=False
        )

        plates = []

        for result in results:

            if result.boxes is None:
                continue

            for box in result.boxes:

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                confidence = float(box.conf[0])

                h, w = frame.shape[:2]

                x1 = max(0, x1)
                y1 = max(0, y1)
                x2 = min(w, x2)
                y2 = min(h, y2)

                if x2 <= x1 or y2 <= y1:
                    continue

                plate_crop = frame[y1:y2, x1:x2]

                plates.append({
                    "bbox": (x1, y1, x2, y2),
                    "confidence": confidence,
                    "crop": plate_crop
                })

        return plates