# ============================================================
#  utils/helpers.py — General Utility Functions
# ============================================================

import os
import cv2
import datetime
import config


def get_timestamp(fmt="%Y-%m-%d %H:%M:%S"):
    """Return the current timestamp as a formatted string."""
    return datetime.datetime.now().strftime(fmt)


def get_date_str():
    return datetime.datetime.now().strftime("%Y-%m-%d")


def save_snapshot(frame, label="unknown"):
    """Save a frame to the snapshots directory."""
    if not config.SAVE_SNAPSHOTS:
        return None

    os.makedirs(config.SNAPSHOT_DIR, exist_ok=True)
    ts  = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{config.SNAPSHOT_DIR}/{label}_{ts}.jpg"
    cv2.imwrite(filename, frame)
    print(f"[Snapshot] Saved → {filename}")
    return filename


def ensure_dirs():
    """Create all required project directories if they don't exist."""
    dirs = [
        config.SNAPSHOT_DIR,
        "logs",
        "models",
        "dataset",
    ]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
