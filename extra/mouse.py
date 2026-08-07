import cv2
import numpy as np

canvas = np.zeros((600, 800, 3), dtype=np.uint8)
drawing = False

def paint(event, x, y, flags, param):
    global drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        cv2.circle(canvas, (x, y), 4, (0, 255, 0), -1)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False

cv2.namedWindow("Paint")
cv2.setMouseCallback("Paint", paint)

while True:
    cv2.imshow("Paint", canvas)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('c'):
        canvas[:] = 0
    elif key == ord('s'):
        cv2.imwrite("drawing.png", canvas)
        print("Saved!")
    elif key == 27:
        break

    # Break if the window's X button was clicked
    if cv2.getWindowProperty("Paint", cv2.WND_PROP_VISIBLE) < 1:
        break

cv2.destroyAllWindows()