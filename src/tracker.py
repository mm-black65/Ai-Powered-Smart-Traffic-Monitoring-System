import math


class VehicleTracker:
    """
    Centroid-based multi-object tracker.

    Tracks are matched frame-to-frame by nearest centroid distance,
    restricted to detections of the SAME class. Tracks survive a few
    missed frames instead of being wiped instantly, and each track
    keeps a trajectory (history of centroids) for use in Phase 2
    (speed) and beyond.

    Two extra guards keep the "unique vehicle" count honest on mostly
    static scenes with small/distant vehicles:
      - Detections below `min_confidence` are shown but never create
        or match a track -- low-confidence boxes are exactly where
        YOLO flickers frame to frame, and that flicker is what was
        inflating the unique-vehicle count.
      - The matching distance threshold scales with the detection's
        own box size (via `distance_scale`, clamped between
        `min_distance` and `max_distance`) instead of being one flat
        number, so a small distant car isn't held to the same pixel
        tolerance as a large nearby one.
      - Each track can only be claimed by ONE detection per frame.
        Without this, two near-duplicate boxes from the detector (a
        known YOLO NMS edge case) could both match the same existing
        track and render as two overlapping boxes sharing one ID.
    """

    VEHICLE_CLASSES = {"car", "motorcycle", "bus", "truck"}

    def __init__(
        self,
        min_confidence=0.35,
        distance_scale=1.5,
        min_distance=40,
        max_distance=200,
        max_missed_frames=10,
        max_trajectory_length=50,
    ):
        self.next_id = 1
        self.tracks = {}  # track_id -> {"center", "class_name", "trajectory", "missed"}
        self.min_confidence = min_confidence
        self.distance_scale = distance_scale
        self.min_distance = min_distance
        self.max_distance = max_distance
        self.max_missed_frames = max_missed_frames
        self.max_trajectory_length = max_trajectory_length

    def get_center(self, bbox):
        x1, y1, x2, y2 = bbox
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2
        return center_x, center_y

    def get_match_threshold(self, bbox):
        """Matching tolerance scaled to how big the box is on screen."""
        x1, y1, x2, y2 = bbox
        diagonal = math.hypot(x2 - x1, y2 - y1)
        threshold = diagonal * self.distance_scale
        return max(self.min_distance, min(threshold, self.max_distance))

    def find_closest_track(self, center, class_name, exclude=None):
        """Nearest existing track of the SAME class, skipping any already claimed this frame."""
        exclude = exclude or set()
        closest_id = None
        minimum_distance = float("inf")

        for track_id, track in self.tracks.items():
            if track_id in exclude:
                continue

            if track["class_name"] != class_name:
                continue

            distance = math.dist(center, track["center"])

            if distance < minimum_distance:
                minimum_distance = distance
                closest_id = track_id

        return closest_id, minimum_distance

    def update(self, detections):
        updated_detections = []
        matched_ids = set()

        for detection in detections:
            class_name = detection["class_name"]

            if class_name not in self.VEHICLE_CLASSES:
                updated_detections.append(detection)
                continue

            if detection["confidence"] < self.min_confidence:
                # Still shown in the frame, just excluded from tracking.
                updated_detections.append(detection)
                continue

            bbox = detection["bbox"]
            center = self.get_center(bbox)
            threshold = self.get_match_threshold(bbox)

            closest_id, distance = self.find_closest_track(center, class_name, exclude=matched_ids)

            if closest_id is not None and distance <= threshold:
                track_id = closest_id
            else:
                track_id = self.next_id
                self.next_id += 1
                self.tracks[track_id] = {
                    "center": center,
                    "class_name": class_name,
                    "trajectory": [],
                    "missed": 0,
                }

            track = self.tracks[track_id]
            track["center"] = center
            track["class_name"] = class_name
            track["missed"] = 0
            track["trajectory"].append(center)
            if len(track["trajectory"]) > self.max_trajectory_length:
                track["trajectory"].pop(0)

            matched_ids.add(track_id)

            detection["track_id"] = track_id
            detection["trajectory"] = track["trajectory"]
            updated_detections.append(detection)

        # Age out unmatched tracks instead of deleting everything each
        # frame -- this is what lets an ID survive a brief occlusion.
        stale_ids = []
        for track_id, track in self.tracks.items():
            if track_id in matched_ids:
                continue
            track["missed"] += 1
            if track["missed"] > self.max_missed_frames:
                stale_ids.append(track_id)

        for track_id in stale_ids:
            del self.tracks[track_id]

        return updated_detections

    def get_trajectory(self, track_id):
        track = self.tracks.get(track_id)
        return track["trajectory"] if track else []