# app.py — Entry point
from app import create_app, db

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    print("🚀 Starting MPLAD Dashboard...")
    print("📍 Open: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)