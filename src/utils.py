import cv2
FONT_SCALE = 1.0
FONT_THICKNESS = 2
BOX_THICKNESS = 3

COLORS = {
    "person": (255, 255, 0),
    "car": (0, 255, 0),
    "motorcycle": (255, 0, 255),
    "bus": (0, 165, 255),
    "truck": (0, 0, 255),
    "traffic light": (255, 0, 0)
}


def draw_detection(frame, detection, occupied_labels=None):

    x1, y1, x2, y2 = detection["bbox"]

    class_name = detection["class_name"]

    confidence = detection["confidence"]

    violation = detection.get("violation", False)

    color = COLORS.get(class_name, (255, 255, 255))
    box_thickness = BOX_THICKNESS

    if violation:
        color = (0, 0, 255)
        box_thickness = BOX_THICKNESS + 3

    track_id = detection.get("track_id")
    speed_kmh = detection.get("speed_kmh")
    lane = detection.get("lane")
    plate = detection.get("plate")

    if track_id is not None:
      label = f"{class_name.upper()} #{track_id} {confidence:.0%}"
      if speed_kmh is not None:
        label += f" {speed_kmh:.0f}km/h"
      if lane is not None:
        label += f" L{lane}"
      if plate:
        label += f" [{plate}]"
      if violation:
        label += " VIOLATION"
    else:
      label = f"{class_name.upper()} {confidence:.0%}"
    (text_width, text_height), baseline = cv2.getTextSize(
      label,
      cv2.FONT_HERSHEY_SIMPLEX,
      FONT_SCALE,
      FONT_THICKNESS
)
    cv2.rectangle(
        frame,
        (x1, y1),
        (x2, y2),
        color,
        box_thickness
    )

    label_height = text_height + 15
    label_width = text_width + 10
    label_left = x1
    label_top = y1 - label_height

    if occupied_labels is not None:
        # Push the label straight down, one label-height at a time,
        # until it clears every label already placed this frame --
        # this is what stops packed detections from stacking illegible
        # text on top of each other.
        while any(
            label_left < ox2 and label_left + label_width > ox1
            and label_top < oy2 and label_top + label_height > oy1
            for (ox1, oy1, ox2, oy2) in occupied_labels
        ):
            label_top += label_height

        occupied_labels.append(
            (label_left, label_top, label_left + label_width, label_top + label_height)
        )

    cv2.rectangle(
        frame,
        (label_left, label_top),
        (label_left + label_width, label_top + label_height),
        color,
       -1
    )
    cv2.putText(
        frame,
        label,
        (label_left + 5, label_top + label_height - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        FONT_SCALE,
        (255, 255, 255),
        FONT_THICKNESS
    )
def count_objects(detections):

    counts = {
        "car": 0,
        "motorcycle": 0,
        "bus": 0,
        "truck": 0,
        "person": 0,
        "traffic light": 0
    }

    for detection in detections:

        name = detection["class_name"]

        if name in counts:
            counts[name] += 1

    return counts

def draw_statistics(frame, counts):

    y = 35

    cv2.putText(
        frame,
        "Smart Traffic Monitoring",
        (20, y),
        cv2.FONT_HERSHEY_SIMPLEX,
        FONT_SCALE,
        (255, 255, 255),
        FONT_THICKNESS
    )

    y += 40

    for key, value in counts.items():

        text = f"{key.title()}: {value}"

        cv2.putText(
            frame,
            text,
            (20, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            COLORS[key],
            2
        )

        y += 30

def draw_unique_vehicle_count(frame, count):

    cv2.putText(
        frame,
        f"Unique Vehicles: {count}",
        (20, 300),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

def draw_lane_counts(frame, lane_counts):

    y = 335

    for lane_number in sorted(lane_counts):

        text = f"Lane {lane_number}: {len(lane_counts[lane_number])}"

        cv2.putText(
            frame,
            text,
            (20, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )

        y += 30

TRAFFIC_LIGHT_STATE_COLORS = {
    "red": (0, 0, 255),
    "yellow": (0, 255, 255),
    "green": (0, 255, 0),
    "unknown": (200, 200, 200)
}

def draw_traffic_light_state(frame, state):

    frame_width = frame.shape[1]

    text = f"Signal: {state.upper()}"

    color = TRAFFIC_LIGHT_STATE_COLORS.get(state, (255, 255, 255))

    cv2.putText(
        frame,
        text,
        (frame_width - 320, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.0,
        color,
        2
    )

def draw_violation_count(frame, count):

    frame_width = frame.shape[1]

    cv2.putText(
        frame,
        f"Violations: {count}",
        (frame_width - 320, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 0, 255),
        2
    )