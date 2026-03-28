# ============================================================
#  automation/alert.py — Email & SMS Alert System
# ============================================================

import smtplib
import time
import os
from email.mime.text      import MIMEText
from email.mime.multipart  import MIMEMultipart
from email.mime.image      import MIMEImage
import config

# Cooldown tracker — avoid repeated alerts for the same event
_last_alert_time: float = 0.0


def _cooldown_ok() -> bool:
    global _last_alert_time
    now = time.time()
    if now - _last_alert_time >= config.ALERT_COOLDOWN_SEC:
        _last_alert_time = now
        return True
    return False


# ── Email ─────────────────────────────────────────────────────────────────────

def send_email_alert(subject: str, body: str, image_path: str = None):
    """
    Send an email alert using Gmail SMTP.

    Args:
        subject    : Email subject line.
        body       : Plain-text email body.
        image_path : Optional path to attach a snapshot image.
    """
    if not config.ALERT_ON_UNKNOWN or not _cooldown_ok():
        return
    if not config.EMAIL_SENDER:
        print("[Alert] EMAIL_SENDER not configured. Skipping email.")
        return

    try:
        msg = MIMEMultipart()
        msg["From"]    = config.EMAIL_SENDER
        msg["To"]      = config.EMAIL_RECEIVER
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Attach snapshot if provided
        if image_path and os.path.isfile(image_path):
            with open(image_path, "rb") as f:
                img = MIMEImage(f.read(), name=os.path.basename(image_path))
                msg.attach(img)

        with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.login(config.EMAIL_SENDER, config.EMAIL_PASSWORD)
            server.sendmail(config.EMAIL_SENDER, config.EMAIL_RECEIVER, msg.as_string())

        print(f"[Alert] Email sent → {config.EMAIL_RECEIVER}")

    except Exception as e:
        print(f"[Alert] Email failed: {e}")


# ── SMS (Twilio) ───────────────────────────────────────────────────────────────

def send_sms_alert(message: str):
    """
    Send an SMS alert via Twilio.

    Args:
        message : Text message body.
    """
    if not config.TWILIO_SID:
        print("[Alert] Twilio not configured. Skipping SMS.")
        return
    try:
        from twilio.rest import Client
        client = Client(config.TWILIO_SID, config.TWILIO_TOKEN)
        client.messages.create(
            body=message,
            from_=config.TWILIO_FROM,
            to=config.TWILIO_TO,
        )
        print(f"[Alert] SMS sent → {config.TWILIO_TO}")
    except Exception as e:
        print(f"[Alert] SMS failed: {e}")


# ── Convenience ───────────────────────────────────────────────────────────────

def trigger_unknown_alert(snapshot_path: str = None):
    """Trigger both email and SMS alert for an unknown face detection."""
    from utils.helpers import get_timestamp
    ts      = get_timestamp()
    subject = f"⚠️ Smart Vision Alert — Unknown Face Detected [{ts}]"
    body    = (
        f"An unrecognised face was detected at {ts}.\n"
        "Please review the attached snapshot.\n\n"
        "— Smart Vision System"
    )
    send_email_alert(subject, body, image_path=snapshot_path)
    send_sms_alert(f"Smart Vision Alert: Unknown face detected at {ts}.")
