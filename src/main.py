import json
import os

import cv2
from detector import TrafficDetector
from utils import draw_detection
from utils import count_objects
from utils import draw_statistics
from utils import draw_unique_vehicle_count
from utils import draw_lane_counts
from utils import draw_traffic_light_state
from utils import draw_violation_count
from tracker import VehicleTracker
from speed_estimator import SpeedEstimator
from lanes import LaneMapper
from lanes import draw_stop_line
from traffic_light import get_state
from plate_detector import LicensePlateDetector
from ocr import LicensePlateOCR

detector = TrafficDetector()
tracker = VehicleTracker()
plate_detector = LicensePlateDetector()
plate_ocr = LicensePlateOCR()
seen_vehicles = set()
lane_counts = {}
vehicle_side = {}
violations = set()
vehicle_plates = {}  # track_id -> (plate_text, ocr_confidence)
traffic_light_state = "unknown"
frame_index = 0

# Plate reading is expensive (a second YOLO pass + full OCR per vehicle),
# so it's throttled rather than run on every vehicle every frame:
MIN_VEHICLE_BOX_AREA_FOR_PLATE = 6000  # skip small/distant vehicles -- plates won't be legible
PLATE_RETRY_EVERY_N_FRAMES = 15        # don't retry a vehicle's plate every single frame
CONFIDENT_PLATE_THRESHOLD = 0.6        # stop retrying once a reading is this confident

video = cv2.VideoCapture("../videos/video1.mp4")
frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(video.get(cv2.CAP_PROP_FPS)) or 30

# --- Speed calibration --------------------------------------------------
# Run `python calibrate.py` once per camera/video to generate this file:
# it has you click the 4 corners of a rectangular patch of road and enter
# its real-world width/length in meters, then saves the resulting
# perspective calibration here.
CALIBRATION_FILE = "calibration.json"

if os.path.exists(CALIBRATION_FILE):
    with open(CALIBRATION_FILE) as f:
        calibration = json.load(f)
    image_points = calibration["image_points"]
    world_points = calibration["world_points"]
    num_lanes = calibration.get("num_lanes", 1)
else:
    # Placeholder covering the full frame as a 10m x 40m patch -- speeds
    # will be inaccurate until you run calibrate.py for this footage.
    image_points = [(0, frame_height), (frame_width, frame_height), (frame_width, 0), (0, 0)]
    world_points = [(0, 0), (10, 0), (10, 40), (0, 40)]
    num_lanes = 1
    print(f"No {CALIBRATION_FILE} found -- using placeholder calibration.")
    print("Run `python calibrate.py` for accurate speeds and lanes on this video.")

speed_estimator = SpeedEstimator(image_points, world_points, fps=fps)

road_width_m = world_points[1][0]
road_length_m = world_points[2][1]
lane_mapper = LaneMapper(speed_estimator, road_width_m, road_length_m, num_lanes)

# --- Stop line (Phase 4) -------------------------------------------------
# Using the "near" edge of the Phase 2 calibration rectangle, i.e. world
# y = road_length_m -- the bottom-left/bottom-right points you clicked
# (closer to the camera). If the drawn stop line lands on the wrong
# side of the road when you run this, set STOP_LINE_WORLD_Y = 0 instead
# to use the far edge (top-left/top-right points).
STOP_LINE_WORLD_Y = road_length_m

fourcc = cv2.VideoWriter_fourcc(*"mp4v")

writer = cv2.VideoWriter(
    "../output/output.mp4",
    fourcc,
    fps,
    (frame_width, frame_height)
)

while True:
    success, frame = video.read()

    if not success:
        break

    detections = detector.detect(frame)
    detections = tracker.update(detections)
    detections.sort(key=lambda d: d["bbox"][0])

    # Keep the last known state if no traffic light is detected this frame
    # rather than flickering back to "unknown".
    traffic_light_detections = [d for d in detections if d["class_name"] == "traffic light"]
    if traffic_light_detections:
        best_light = max(traffic_light_detections, key=lambda d: d["confidence"])
        traffic_light_state = get_state(frame, best_light["bbox"])

    occupied_labels = []

    for detection in detections:
        track_id = detection.get("track_id")

        if track_id is not None:
            seen_vehicles.add(track_id)

            trajectory = detection.get("trajectory")
            if trajectory:
                speed_kmh = speed_estimator.estimate_speed_kmh(trajectory)
                if speed_kmh is not None:
                    detection["speed_kmh"] = speed_kmh

                world_x, world_y = speed_estimator.to_world(trajectory[-1])
                lane = lane_mapper.lane_for_x(world_x)
                if lane is not None:
                    detection["lane"] = lane
                    lane_counts.setdefault(lane, set()).add(track_id)

                current_side = "before" if world_y < STOP_LINE_WORLD_Y else "after"
                previous_side = vehicle_side.get(track_id)

                if previous_side is not None and previous_side != current_side and traffic_light_state == "red":
                    violations.add(track_id)

                vehicle_side[track_id] = current_side

            vx1, vy1, vx2, vy2 = detection["bbox"]
            box_area = (vx2 - vx1) * (vy2 - vy1)
            existing_plate = vehicle_plates.get(track_id)
            already_confident = existing_plate is not None and existing_plate[1] >= CONFIDENT_PLATE_THRESHOLD

            should_attempt_plate = (
                not already_confident
                and box_area >= MIN_VEHICLE_BOX_AREA_FOR_PLATE
                and frame_index % PLATE_RETRY_EVERY_N_FRAMES == 0
            )

            if should_attempt_plate:
                vehicle_crop = frame[vy1:vy2, vx1:vx2]
                plates = plate_detector.detect(vehicle_crop)

                if plates:
                    best_plate = max(plates, key=lambda p: p["confidence"])
                    text, ocr_confidence = plate_ocr.read(best_plate["crop"])

                    if text and (existing_plate is None or ocr_confidence > existing_plate[1]):
                        vehicle_plates[track_id] = (text, ocr_confidence)

            plate_info = vehicle_plates.get(track_id)
            if plate_info is not None:
                detection["plate"] = plate_info[0]

            if track_id in violations:
                detection["violation"] = True

        draw_detection(frame, detection, occupied_labels)

    lane_mapper.draw_lanes(frame)
    draw_stop_line(frame, speed_estimator, road_width_m, STOP_LINE_WORLD_Y)

    draw_unique_vehicle_count(frame, len(seen_vehicles))
    draw_lane_counts(frame, lane_counts)
    draw_traffic_light_state(frame, traffic_light_state)
    draw_violation_count(frame, len(violations))

    counts = count_objects(detections)
    draw_statistics(frame, counts)

    writer.write(frame)

    frame_index += 1

    display_frame = cv2.resize(frame, (1280, 720))
    cv2.imshow("Smart Traffic Monitoring", display_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video.release()
writer.release()
cv2.destroyAllWindows()