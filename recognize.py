#!/usr/bin/env python3
# ============================================================
#  recognize.py — Real-time Face Recognition + Automation
# ============================================================
#
#  USAGE:
#      python recognize.py
#
#  Prerequisites:
#      1. Run `python train.py` first to build face encodings.
#      2. Configure .env with email/SMS credentials.
#
#  Press Q to quit.
# ============================================================

import os
import pickle
import cv2
import face_recognition
import numpy as np
import config

from utils.camera  import Camera
from utils.draw    import draw_face_box, draw_status
from utils.helpers import ensure_dirs, save_snapshot, get_timestamp
from automation.attendance import log_attendance
from automation.alert      import trigger_unknown_alert


def load_encodings(path: str):
    """Load known face encodings from pickle file."""
    if not os.path.isfile(path):
        raise FileNotFoundError(
            f"Encodings file not found: {path}\n"
            "Run `python train.py` first."
        )
    with open(path, "rb") as f:
        data = pickle.load(f)
    print(f"[Recognize] Loaded {len(data['names'])} encoding(s) "
          f"for {len(set(data['names']))} person(s).")
    return data["encodings"], data["names"]


def identify_face(face_encoding, known_encodings, known_names) -> str:
    """
    Compare a face encoding against known encodings.

    Returns the matched person's name or UNKNOWN_LABEL.
    """
    if not known_encodings:
        return config.UNKNOWN_LABEL

    distances = face_recognition.face_distance(known_encodings, face_encoding)
    best_idx  = int(np.argmin(distances))

    if distances[best_idx] <= (1 - config.CONFIDENCE_THRESHOLD):
        return known_names[best_idx]
    return config.UNKNOWN_LABEL


def main():
    ensure_dirs()

    # Load trained encodings
    known_encodings, known_names = load_encodings(config.ENCODINGS_PATH)

    print("[Recognize] Starting recognition... Press Q to quit.\n")

    with Camera() as cam:
        while True:
            ret, frame = cam.read()
            if not ret:
                print("[Recognize] Failed to read frame.")
                break

            # Downscale for performance
            small  = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
            rgb    = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

            # Detect faces
            face_locations = face_recognition.face_locations(
                rgb, model=config.DETECTION_MODEL
            )
            face_encodings = face_recognition.face_encodings(rgb, face_locations)

            for face_enc, (top, right, bottom, left) in zip(face_encodings, face_locations):
                # Scale coordinates back to full frame
                top    *= 2; right  *= 2
                bottom *= 2; left   *= 2

                name = identify_face(face_enc, known_encodings, known_names)

                # Draw bounding box
                draw_face_box(frame, top, right, bottom, left, name)

                # ── Automation Triggers ──────────────────────────────
                if name != config.UNKNOWN_LABEL:
                    log_attendance(name)
                else:
                    snapshot = save_snapshot(frame, label="unknown")
                    trigger_unknown_alert(snapshot_path=snapshot)
                # ────────────────────────────────────────────────────

            # Status bar
            ts = get_timestamp("%H:%M:%S")
            draw_status(frame, f"Smart Vision  |  {ts}  |  Faces: {len(face_locations)}")

            cv2.imshow("Smart Vision — Recognition", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    cv2.destroyAllWindows()
    print("[Recognize] Stopped.")


if __name__ == "__main__":
    main()
