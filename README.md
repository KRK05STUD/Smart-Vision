# 🔍 Smart Vision — Face Detection & Automation System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?style=for-the-badge&logo=opencv)
![DeepFace](https://img.shields.io/badge/DeepFace-Latest-orange?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

> A real-time face detection and recognition system built with Python, OpenCV, and automation pipelines — designed for smart surveillance, attendance tracking, and access control applications.

---

## 📌 Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Automation Pipeline](#automation-pipeline)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## 📖 About the Project

**Smart Vision** is a Python-based intelligent computer vision system that performs real-time face detection and recognition using a live camera feed or video input. It integrates automation tools to trigger actions such as sending alerts, logging attendance, and controlling access — all without manual intervention.

This project is ideal for:
- 🏢 Office attendance and access management
- 🏫 School/college automated attendance systems
- 🔐 Smart security surveillance
- 🏠 Home automation and smart door systems

---

## ✨ Features

- ✅ Real-time face detection using OpenCV and Haar Cascade / DNN models
- ✅ Face recognition with DeepFace / face_recognition library
- ✅ Automated attendance logging to CSV / Excel / Database
- ✅ Email/SMS alert triggers on unknown face detection
- ✅ Multi-face detection in a single frame
- ✅ Live webcam and IP camera support
- ✅ Bounding box drawing with name labels
- ✅ Face encoding and training on custom datasets
- ✅ Configurable confidence thresholds
- ✅ Logging with timestamps and snapshots
- ✅ Modular automation pipeline (easily extendable)

---

## 🛠️ Tech Stack

| Category | Tools / Libraries |
|---|---|
| Language | Python 3.8+ |
| Computer Vision | OpenCV, face_recognition |
| Deep Learning | DeepFace, TensorFlow / PyTorch |
| Automation | schedule, smtplib, Twilio |
| Data Storage | CSV, SQLite, Excel (openpyxl) |
| Notifications | Email (SMTP), SMS (Twilio API) |
| UI (Optional) | Tkinter / Flask Web Dashboard |
| Environment | dotenv, argparse |

---

## 📁 Project Structure

```
smart-vision/
│
├── 📂 dataset/                  # Training face images (organized by person name)
│   ├── Person_1/
│   └── Person_2/
│
├── 📂 models/                   # Trained face encodings and models
│   └── face_encodings.pkl
│
├── 📂 logs/                     # Attendance logs and snapshots
│   ├── attendance.csv
│   └── snapshots/
│
├── 📂 automation/               # Automation scripts
│   ├── alert.py                 # Email/SMS alert system
│   ├── attendance.py            # Attendance logging module
│   └── scheduler.py             # Scheduled task runner
│
├── 📂 utils/                    # Utility functions
│   ├── camera.py                # Camera/video feed handler
│   ├── draw.py                  # Bounding box and label drawing
│   └── helpers.py               # General helpers
│
├── 📄 train.py                  # Train face recognition model on dataset
├── 📄 detect.py                 # Main face detection script
├── 📄 recognize.py              # Face recognition with automation triggers
├── 📄 app.py                    # (Optional) Flask web dashboard
│
├── 📄 config.py                 # Configuration variables
├── 📄 requirements.txt          # Python dependencies
├── 📄 .env.example              # Environment variables template
└── 📄 README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or above
- pip (Python package manager)
- A webcam or IP camera
- (Optional) GPU with CUDA for faster deep learning inference

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/smart-vision.git
   cd smart-vision
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate        # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials (email, Twilio API, etc.)
   ```

### Configuration

Edit `config.py` to customize:
```python
CAMERA_SOURCE = 0              # 0 for webcam, or IP camera URL
CONFIDENCE_THRESHOLD = 0.6     # Face recognition confidence level
ALERT_ON_UNKNOWN = True        # Trigger alert for unknown faces
SAVE_SNAPSHOTS = True          # Save snapshot on detection
LOG_FILE = "logs/attendance.csv"
```

---

## 💻 Usage

### Step 1 — Add face data to the dataset
```bash
# Organize images in dataset/Person_Name/ folders
# Example:
mkdir dataset/John_Doe
# Add 10-20 clear face images of John to that folder
```

### Step 2 — Train the model
```bash
python train.py
```

### Step 3 — Run face detection & recognition
```bash
python recognize.py
```

### Step 4 — Run detection only (no recognition)
```bash
python detect.py
```

### Optional — Start the web dashboard
```bash
python app.py
# Visit http://localhost:5000
```

---

## ⚙️ How It Works

```
📷 Camera Feed
     ↓
🔲 Face Detection (OpenCV / DNN)
     ↓
📐 Face Encoding (face_recognition / DeepFace)
     ↓
🔍 Match Against Known Encodings
     ↓
✅ Known Face → Log Attendance + Display Name
❌ Unknown Face → Trigger Alert + Save Snapshot
     ↓
📊 Store Results (CSV / Database)
```

---

## 🤖 Automation Pipeline

| Trigger | Action |
|---|---|
| Known face detected | Log to attendance CSV with timestamp |
| Unknown face detected | Send email/SMS alert with snapshot |
| Multiple attempts | Lock entry and notify admin |
| Scheduled reports | Daily attendance summary email |
| Low confidence match | Flag for manual review |

---

## 📸 Screenshots

> *(Add your screenshots here)*

| Live Detection | Attendance Log | Alert Email |
|---|---|---|
| ![detect](screenshots/detect.png) | ![log](screenshots/log.png) | ![alert](screenshots/alert.png) |

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes and commit: `git commit -m "Add: your feature description"`
4. Push to your branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

Please follow the existing code style and add comments where necessary.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 📬 Contact

**Your Name**
- GitHub: [@your-username](https://github.com/your-username)
- Email: your.email@example.com
- LinkedIn: [your-linkedin](https://linkedin.com/in/your-profile)

---

<p align="center">
  Made with ❤️ using Python & Computer Vision
</p>
