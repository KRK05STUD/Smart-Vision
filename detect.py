#!/usr/bin/env python3
# ============================================================
#  detect.py — Real-time Face Detection (No Recognition)
# ============================================================
#
#  USAGE:
#      python detect.py
#
#  Press Q to quit.
# ============================================================

import cv2
import face_recognition
import config
from utils.camera  import Camera
from utils.draw    import draw_face_box, draw_status
from utils.helpers import ensure_dirs


def main():
    ensure_dirs()
    print("[Detect] Starting face detection... Press Q to quit.")

    with Camera() as cam:
        while True:
            ret, frame = cam.read()
            if not ret:
                print("[Detect] Failed to read frame.")
                break

            # Resize for faster processing, then scale locations back
            small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            rgb_small   = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            # Detect face locations
            face_locations = face_recognition.face_locations(
                rgb_small, model=config.DETECTION_MODEL
            )

            # Draw boxes
            for (top, right, bottom, left) in face_locations:
                # Scale back up
                top    *= 2
                right  *= 2
                bottom *= 2
                left   *= 2
                draw_face_box(frame, top, right, bottom, left, "Face")

            # Status overlay
            count = len(face_locations)
            draw_status(frame, f"Faces Detected: {count}")

            cv2.imshow("Smart Vision — Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cv2.destroyAllWindows()
    print("[Detect] Stopped.")


if __name__ == "__main__":
    main()
