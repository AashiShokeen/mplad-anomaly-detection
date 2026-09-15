# 🏛️ Anomaly X — MPLAD Anomaly Detection

**🔗 Live Demo:** [https://anomaly-x.onrender.com](https://anomaly-x.onrender.com)

[![Live Demo](https://img.shields.io/badge/demo-live-success)](https://anomaly-x.onrender.com)
[![Python](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-2.3-lightgrey)](https://flask.palletsprojects.com/)
[![SIH 2026](https://img.shields.io/badge/SIH-2026-orange)](https://sih.gov.in/)

Live audit engine for MPLAD public spending. Detects cost outliers, stalled projects, and duplicate works — with explainable, plain-language reasons.

**SIH 2026 · Problem SIH26102 · Team Anomaly X**

> **Demo login:** `admin` / `admin123`

---

## 🎯 What It Does

- Reads MPLAD records from eSAKSHI-style CSV
- Runs detection rules:
  - **Cost outliers** — projects > 3x category median
  - **Stalled projects** — pending > 180 days with > ₹5L
  - **Duplicates** — same work sanctioned twice in same village
- Displays live dashboard with real statistics
- Every flag explained with confidence score & audit evidence (XAI modal)
- Exports real CSV & PDF reports for CAG/Ministry review

## 🚀 Quick Start

### 1. Clone and set up

\`\`\`bash
git clone https://github.com/AashiShokeen/mplad-anomaly-detection.git
cd mplad-anomaly-detection
python -m venv venv
venv\Scripts\activate     # Windows
# source venv/bin/activate # Mac/Linux
pip install -r requirements.txt
\`\`\`

### 2. Load data and run detection

\`\`\`bash
python load_csv.py        # Load CSV → SQLite (~100 projects)
python run_detection.py   # Create anomalies (~55 flags)
python create_admin.py    # Create admin + officer users
\`\`\`

### 3. Run the app

\`\`\`bash
python run.py
\`\`\`

Open: **http://127.0.0.1:5000**

Login: **admin / admin123**

---

## 📄 Pages

| Route | What It Shows |
| :--- | :--- |
| `/dashboard` | Live stats, pie chart, top districts, cost outliers |
| `/flagged` | 55 detected anomalies with reasons |
| `/projects` | All 100 MPLAD projects |
| `/analytics` | District-wise comparison |
| `/login` | Authentication |

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Backend** | Python, Flask, Flask-Login, SQLAlchemy |
| **Database** | SQLite |
| **Frontend** | Tailwind CSS, HTML, Chart.js, Bootstrap Icons |
| **Detection** | Python (statistics, difflib) |
| **Exports** | reportlab (PDF), csv (spreadsheets) |
| **Deployment** | Render (auto-seed on boot) |

---

## 📁 Project Structure

\`\`\`
mplad-anomaly-detection/
├── app/
│   ├── __init__.py       # Flask app factory + auto-seed
│   ├── models.py         # SQLAlchemy models
│   ├── routes.py         # Page + API + export routes
│   ├── auth.py           # Login/logout
│   └── anomaly.py        # Detection logic
├── templates/            # HTML pages (Jinja)
├── static/
│   ├── css/style.css
│   └── js/
├── data/
│   └── mplad_cleaned_final.csv
├── instance/
│   └── mplads.db         # Pre-built demo DB (shipped to Render)
├── load_csv.py           # Load CSV → DB
├── run_detection.py      # Run anomaly detection
├── create_admin.py       # Create admin user
├── run.py                # App entry point
├── Procfile              # Render start command
└── requirements.txt
\`\`\`

---

## ✨ Key Features

- 🚩 **Explainable AI (XAI) modal** — every anomaly shows confidence, rule triggered, and evidence logs
- 🔗 **Duplicate Detector** — side-by-side comparison of suspected double-funded works
- ✅ **Audit workflow** — Under Review → Disbursement Frozen → Resolved
- 👁️ **Show/Hide reviewed toggle** — full audit trail, nothing deleted
- 📄 **Real exports** — CSV ledgers and formatted PDF audit reports
- 🌐 **Live on Render** — auto-seeds data on every boot

---

## 👥 Team

| Member | Role |
| :--- | :--- |
| **Aashi** | Integration + Dashboard + Backend |
| **Rohanshi** | Backend APIs + SQL |
| **Vanshika** | Data + Detection logic |
| **Bhoomi** | Frontend + Styling |
| **Anshika** | Auth + Templates |
| **Aditi** | UI/UX + Design |

---

## 📊 Impact

- **Not just a dashboard** — a live audit engine
- **Every flag has a reason** — verifiable, explainable
- **Built for MPLAD** — extensible to every public spending scheme
- **Rule-based today** — ML + NLP layers planned for v2

---

*Built for Smart India Hackathon 2026*