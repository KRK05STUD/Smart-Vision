# ============================================================
#  Smart Vision — Central Configuration
# ============================================================

import os
from dotenv import load_dotenv

load_dotenv()

# --- Camera ---
CAMERA_SOURCE = 0                  # 0 = webcam | "rtsp://..." = IP cam
FRAME_WIDTH   = 640
FRAME_HEIGHT  = 480
FPS           = 30

# --- Face Detection ---
DETECTION_MODEL      = "hog"       # "hog" (CPU) | "cnn" (GPU, more accurate)
CONFIDENCE_THRESHOLD = 0.55        # 0.0 – 1.0  (lower = stricter)
SCALE_FACTOR         = 1.1
MIN_NEIGHBORS        = 5

# --- Recognition ---
ENCODINGS_PATH  = "models/face_encodings.pkl"
DATASET_DIR     = "dataset"
UNKNOWN_LABEL   = "Unknown"

# --- Logging & Snapshots ---
LOG_FILE         = "logs/attendance.csv"
SNAPSHOT_DIR     = "logs/snapshots"
SAVE_SNAPSHOTS   = True            # Save image on unknown face

# --- Alerts ---
ALERT_ON_UNKNOWN    = True
ALERT_COOLDOWN_SEC  = 60           # Min seconds between repeated alerts

# --- Email (SMTP) ---
EMAIL_SENDER    = os.getenv("EMAIL_SENDER", "")
EMAIL_PASSWORD  = os.getenv("EMAIL_PASSWORD", "")
EMAIL_RECEIVER  = os.getenv("EMAIL_RECEIVER", "")
SMTP_HOST       = "smtp.gmail.com"
SMTP_PORT       = 587

# --- Twilio SMS (optional) ---
TWILIO_SID    = os.getenv("TWILIO_SID", "")
TWILIO_TOKEN  = os.getenv("TWILIO_TOKEN", "")
TWILIO_FROM   = os.getenv("TWILIO_FROM", "")
TWILIO_TO     = os.getenv("TWILIO_TO", "")

# --- Display ---
BOX_COLOR_KNOWN   = (0, 255, 0)    # Green
BOX_COLOR_UNKNOWN = (0, 0, 255)    # Red
TEXT_COLOR        = (255, 255, 255)
FONT_SCALE        = 0.6
THICKNESS         = 2
