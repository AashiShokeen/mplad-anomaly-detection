# Anomaly X — MPLAD Anomaly Detection

Live audit engine for MPLAD public spending. Detects cost outliers, stalled projects, and duplicate works — with explainable, plain-language reasons.

**SIH 2026 · Problem SIH26102 · Team Anomaly X**

---

## 🎯 What It Does

- Reads MPLAD records from eSAKSHI-style CSV
- Runs 3 detection rules:
  - **Cost outliers** — projects > 3x category median
  - **Stalled projects** — pending > 180 days with > ₹5L
  - **Duplicates** — similar names in same district
- Displays live dashboard with real statistics
- Interactive tables with filtering and analysis

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
| **Frontend** | HTML, CSS, Bootstrap 5, Chart.js |
| **Detection** | Python (statistics, difflib) |
| **Deployment** | PythonAnywhere / Render |

---

## 📁 Project Structure

\`\`\`
mplad-anomaly-detection/
├── app/
│   ├── __init__.py       # Flask app factory
│   ├── models.py         # SQLAlchemy models
│   ├── routes.py         # Page + API routes
│   ├── auth.py           # Login/logout
│   └── anomaly.py        # Detection logic
├── templates/            # HTML pages
├── static/
│   ├── css/style.css
│   └── js/               # Charts, dashboard scripts
├── data/
│   └── mplad_cleaned_final.csv
├── load_csv.py           # Load CSV → DB
├── run_detection.py      # Run anomaly detection
├── create_admin.py       # Create admin user
├── run.py                # App entry point
└── requirements.txt
\`\`\`

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
