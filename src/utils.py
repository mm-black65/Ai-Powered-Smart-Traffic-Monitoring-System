import cv2


COLORS = {
    "person": (255, 255, 0),
    "car": (0, 255, 0),
    "motorcycle": (255, 0, 255),
    "bus": (0, 165, 255),
    "truck": (0, 0, 255),
    "traffic light": (255, 0, 0)
}


def draw_detection(frame, detection):

    x1, y1, x2, y2 = detection["bbox"]

    class_name = detection["class_name"]

    confidence = detection["confidence"]

    color = COLORS.get(class_name, (255, 255, 255))

    label = f"{class_name} {confidence:.2f}"

    cv2.rectangle(
        frame,
        (x1, y1),
        (x2, y2),
        color,
        2
    )

    cv2.putText(
        frame,
        label,
        (x1, y1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        color,
        2
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
        0.8,
        (255, 255, 255),
        2
    )

    y += 40

    for key, value in counts.items():

        text = f"{key.title()}: {value}"

        cv2.putText(
            frame,
            text,
            (20, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            COLORS[key],
            2
        )

        y += 30