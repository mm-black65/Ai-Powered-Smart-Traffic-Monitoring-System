import math

from numpy.char import center


class VehicleTracker:

        def __init__(self):

            self.next_id = 1
            self.tracks = {}
            self.max_distance = 50
 
        def get_center(self, bbox):
            x1, y1, x2, y2 = bbox

            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2

            return center_x, center_y

        def find_closest_track(self, center):
   
            closest_id = None
            minimum_distance = float("inf")

            for track_id, track_center in self.tracks.items():

                distance = math.dist(center, track_center)

                if distance < minimum_distance:
                    minimum_distance = distance
                    closest_id = track_id

            return closest_id, minimum_distance
        def update(self, detections):

            updated_detections = []
            new_tracks = {}

            for detection in detections:

        # Only track vehicles
              if detection["class_name"] not in {
                 "car",
                 "motorcycle",
                 "bus",
                 "truck"
        }:
               updated_detections.append(detection)
               continue

              center = self.get_center(detection["bbox"])

              closest_id, distance = self.find_closest_track(center)
  
              if closest_id is not None and distance <= self.max_distance:
                track_id = closest_id
              else:
                track_id = self.next_id
                self.next_id += 1

              new_tracks[track_id] = center

              detection["track_id"] = track_id
              updated_detections.append(detection)

            self.tracks = new_tracks

            return updated_detections