# ============================================================
#  utils/draw.py — Bounding Box & Label Drawing
# ============================================================

import cv2
import config


def draw_face_box(frame, top, right, bottom, left, name):
    """
    Draw a labelled bounding box around a detected face.

    Args:
        frame  : The BGR video frame.
        top, right, bottom, left : Face location coordinates.
        name   : Recognised person name or 'Unknown'.
    """
    color = (
        config.BOX_COLOR_KNOWN
        if name != config.UNKNOWN_LABEL
        else config.BOX_COLOR_UNKNOWN
    )

    # Rectangle
    cv2.rectangle(frame, (left, top), (right, bottom), color, config.THICKNESS)

    # Label background
    cv2.rectangle(
        frame,
        (left, bottom - 30),
        (right, bottom),
        color,
        cv2.FILLED,
    )

    # Label text
    cv2.putText(
        frame,
        name,
        (left + 6, bottom - 8),
        cv2.FONT_HERSHEY_DUPLEX,
        config.FONT_SCALE,
        config.TEXT_COLOR,
        1,
    )


def draw_status(frame, text, position=(10, 30), color=(0, 255, 255)):
    """Draw a status message on the top of the frame."""
    cv2.putText(
        frame,
        text,
        position,
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        color,
        2,
    )
