import math

from numpy.char import center


class VehicleTracker:

        def __init__(self):

            self.next_id = 1

            self.tracks = {}
 
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