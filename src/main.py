import cv2 
from detector import TrafficDetector
from utils import draw_detection
from utils import count_objects
from utils import draw_statistics

detector = TrafficDetector()

video = cv2.VideoCapture("../videos/video1.mp4")
frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(video.get(cv2.CAP_PROP_FPS))

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
    for detection in detections:
        draw_detection(frame, detection)
    counts = count_objects(detections)
    draw_statistics(frame, counts)
    display_frame = cv2.resize(frame, (1280, 720))

    cv2.imshow("Smart Traffic Monitoring", display_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
       break

video.release()
writer.release()
cv2.destroyAllWindows()