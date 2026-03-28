#!/usr/bin/env python3
# ============================================================
#  train.py — Build Face Encodings from Dataset
# ============================================================
#
#  USAGE:
#      python train.py
#
#  Dataset structure expected:
#      dataset/
#        ├── Person_Name_1/
#        │     ├── img1.jpg
#        │     └── img2.jpg
#        └── Person_Name_2/
#              └── img1.jpg
# ============================================================

import os
import pickle
import face_recognition
import cv2
import config
from utils.helpers import ensure_dirs

SUPPORTED_EXT = {".jpg", ".jpeg", ".png", ".bmp"}


def load_images_from_dataset(dataset_dir: str):
    """
    Walk the dataset directory and load all face images.

    Returns:
        known_encodings : list of 128-d face encodings
        known_names     : corresponding list of person names
    """
    known_encodings = []
    known_names     = []

    persons = sorted(os.listdir(dataset_dir))
    print(f"[Train] Found {len(persons)} person(s) in dataset.\n")

    for person_name in persons:
        person_dir = os.path.join(dataset_dir, person_name)
        if not os.path.isdir(person_dir):
            continue

        images = [
            f for f in os.listdir(person_dir)
            if os.path.splitext(f)[1].lower() in SUPPORTED_EXT
        ]
        print(f"  → {person_name}: {len(images)} image(s)")

        for img_file in images:
            img_path = os.path.join(person_dir, img_file)
            image    = face_recognition.load_image_file(img_path)
            encodings = face_recognition.face_encodings(
                image, model=config.DETECTION_MODEL
            )

            if encodings:
                known_encodings.append(encodings[0])
                known_names.append(person_name)
            else:
                print(f"    ⚠ No face found in {img_file} — skipping.")

    return known_encodings, known_names


def save_encodings(encodings, names, path: str):
    """Persist encodings to a pickle file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as f:
        pickle.dump({"encodings": encodings, "names": names}, f)
    print(f"\n[Train] Encodings saved → {path}")


def main():
    ensure_dirs()
    print("=" * 50)
    print("  Smart Vision — Training Face Encodings")
    print("=" * 50)

    if not os.path.isdir(config.DATASET_DIR):
        print(f"[Train] Dataset directory '{config.DATASET_DIR}' not found.")
        print("  Create it and add sub-folders per person.")
        return

    encodings, names = load_images_from_dataset(config.DATASET_DIR)

    if not encodings:
        print("[Train] No valid face encodings found. Aborting.")
        return

    save_encodings(encodings, names, config.ENCODINGS_PATH)
    print(f"[Train] Done. {len(encodings)} encoding(s) for {len(set(names))} person(s).")


if __name__ == "__main__":
    main()
