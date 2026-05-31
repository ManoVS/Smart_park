import cv2
from pyzbar.pyzbar import decode
import json


class QRScanner:

    def __init__(self, camera_id=0):

        self.cap = cv2.VideoCapture(camera_id)

        if not self.cap.isOpened():
            raise Exception(
                f"Cannot open camera {camera_id}"
            )

    def read(self):

        ret, frame = self.cap.read()

        if not ret:
            return None

        qr_codes = decode(frame)

        for qr in qr_codes:

            try:

                data = qr.data.decode("utf-8")

                payload = json.loads(data)

                if (
                    "slot" in payload and
                    "ticket" in payload
                ):

                    return {
                        "slot": int(payload["slot"]),
                        "ticket": int(payload["ticket"])
                    }

            except Exception:
                continue

        return None

    def release(self):

        self.cap.release()
