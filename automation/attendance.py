# ============================================================
#  automation/attendance.py — Attendance Logging Module
# ============================================================

import os
import csv
import pandas as pd
from utils.helpers import get_timestamp, get_date_str
import config

# Track who has already been logged today (in memory)
_logged_today: set = set()


def reset_daily_log():
    """Clear the in-memory log (call this at midnight / new session)."""
    _logged_today.clear()


def log_attendance(name: str):
    """
    Log a recognised person's attendance to CSV.
    Each person is logged only once per session.

    Args:
        name : Recognised person's name.
    """
    if name == config.UNKNOWN_LABEL or name in _logged_today:
        return

    _logged_today.add(name)
    os.makedirs("logs", exist_ok=True)

    file_exists = os.path.isfile(config.LOG_FILE)
    with open(config.LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Name", "Date", "Time", "Status"])
        writer.writerow([name, get_date_str(), get_timestamp("%H:%M:%S"), "Present"])

    print(f"[Attendance] Logged → {name} at {get_timestamp()}")


def get_todays_report() -> pd.DataFrame:
    """Return today's attendance as a DataFrame."""
    if not os.path.isfile(config.LOG_FILE):
        return pd.DataFrame(columns=["Name", "Date", "Time", "Status"])
    df = pd.read_csv(config.LOG_FILE)
    return df[df["Date"] == get_date_str()]


def export_to_excel(output_path="logs/attendance_report.xlsx"):
    """Export the full attendance log to an Excel file."""
    if not os.path.isfile(config.LOG_FILE):
        print("[Attendance] No log file found.")
        return
    df = pd.read_csv(config.LOG_FILE)
    df.to_excel(output_path, index=False)
    print(f"[Attendance] Exported to Excel → {output_path}")
