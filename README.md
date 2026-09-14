\# Anomaly X — MPLAD Anomaly Detection



Live audit engine for MPLAD public spending. Detects cost outliers, stalled projects, and duplicates.



\## Quick Start



\### 1. Clone and set up

\\`\\`\\`bash

git clone https://github.com/AashiShokeen/mplad-anomaly-detection.git

cd mplad-anomaly-detection

python -m venv venv

venv\\Scripts\\activate     # Windows

pip install -r requirements.txt

\\`\\`\\`



\### 2. Load data and run detection

\\`\\`\\`bash

python load\_csv.py        # Load CSV into SQLite

python run\_detection.py   # Create anomalies

python create\_admin.py    # Create admin user

\\`\\`\\`



\### 3. Run the app

\\`\\`\\`bash

python run.py

\\`\\`\\`



Open: http://127.0.0.1:5000

Login: admin / admin123



\## Pages



| Route | What |

| :--- | :--- |

| `/dashboard` | Live stats + charts |

| `/flagged` | 55 detected anomalies |

| `/projects` | All 100 MPLAD projects |

| `/analytics` | District comparison |

| `/login` | Authentication |



\## Tech Stack



\- Backend: Flask, SQLAlchemy, Flask-Login

\- Database: SQLite

\- Frontend: HTML, CSS, Bootstrap, Chart.js

\- Detection: Python, statistics, difflib



\## Team



\- Aditi — UI/UX + Design

\- Bhoomi — Styling + Frontend

\- Anshika — Auth + Frontend

\- Vanshika — Data + Detection logic

\- Rohanshi — Backend + APIs

\- Aashi — Integration + Dashboard



SIH 2026 · Problem SIH26102

\\`\\`\\`

