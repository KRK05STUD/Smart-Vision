# ============================================================
#  utils/camera.py — Camera / Video Feed Handler
# ============================================================

import cv2
import config


class Camera:
    def __init__(self, source=None):
        self.source = source if source is not None else config.CAMERA_SOURCE
        self.cap = None

    def start(self):
        """Open the camera stream."""
        self.cap = cv2.VideoCapture(self.source)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,  config.FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS,          config.FPS)
        if not self.cap.isOpened():
            raise RuntimeError(f"Cannot open camera source: {self.source}")
        print(f"[Camera] Started — source: {self.source}")

    def read(self):
        """Read a single frame. Returns (success, frame)."""
        if self.cap is None:
            raise RuntimeError("Camera not started. Call camera.start() first.")
        return self.cap.read()

    def release(self):
        """Release the camera resource."""
        if self.cap:
            self.cap.release()
            print("[Camera] Released.")

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.release()
