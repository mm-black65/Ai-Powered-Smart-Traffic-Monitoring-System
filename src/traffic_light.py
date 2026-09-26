import cv2


def get_state(frame, bbox):
    """
    Crops the detected traffic-light region and classifies its active
    color using HSV thresholds. Returns "red", "yellow", "green", or
    "unknown" if no color has enough lit pixels to be confident.

    HSV thresholding rather than a trained classifier: traffic-light
    housings are small, low-res crops where a lit bulb is essentially
    a solid color blob, which plain color thresholding handles well
    without needing a second model or training data.
    """
    x1, y1, x2, y2 = bbox
    crop = frame[y1:y2, x1:x2]

    if crop.size == 0:
        return "unknown"

    hsv = cv2.cvtColor(crop, cv2.COLOR_BGR2HSV)

    # Red wraps around the hue circle, so it needs two ranges.
    red_mask = (
        cv2.inRange(hsv, (0, 100, 100), (10, 255, 255))
        | cv2.inRange(hsv, (160, 100, 100), (180, 255, 255))
    )
    yellow_mask = cv2.inRange(hsv, (15, 100, 100), (35, 255, 255))
    green_mask = cv2.inRange(hsv, (40, 70, 70), (90, 255, 255))

    pixel_counts = {
        "red": cv2.countNonZero(red_mask),
        "yellow": cv2.countNonZero(yellow_mask),
        "green": cv2.countNonZero(green_mask),
    }

    best_state = max(pixel_counts, key=pixel_counts.get)

    # Tune this if your footage's traffic lights are consistently tiny/blurry.
    MIN_LIT_PIXELS = 5

    if pixel_counts[best_state] < MIN_LIT_PIXELS:
        return "unknown"

    return best_state