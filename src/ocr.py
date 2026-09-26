import cv2
import easyocr
import re


class LicensePlateOCR:

    def __init__(self):
        self.reader = easyocr.Reader(
            ["en"],
            gpu=False
        )

    def preprocess(self, plate):

        gray = cv2.cvtColor(
            plate,
            cv2.COLOR_BGR2GRAY
        )

        gray = cv2.resize(
            gray,
            None,
            fx=2,
            fy=2,
            interpolation=cv2.INTER_CUBIC
        )

        gray = cv2.equalizeHist(gray)

        return gray

    def clean_text(self, text):

        text = text.upper()

        text = re.sub(
            r"[^A-Z0-9]",
            "",
            text
        )

        return text

    def read(self, plate):

        if plate is None or plate.size == 0:
            return None, 0.0

        processed = self.preprocess(plate)

        results = self.reader.readtext(
            processed,
            detail=1
        )

        if not results:
            return None, 0.0

        best_text = None
        best_confidence = 0.0

        for _, text, confidence in results:

            text = self.clean_text(text)

            if confidence > best_confidence:

                best_text = text
                best_confidence = confidence

        return best_text, best_confidence