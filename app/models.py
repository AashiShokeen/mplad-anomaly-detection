# app/models.py
from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    district = db.Column(db.String(100))
    work_category = db.Column(db.String(100))
    amount = db.Column(db.Float)
    village = db.Column(db.String(100))
    sanction_date = db.Column(db.DateTime)
    work_status = db.Column(db.String(50), default='recommended')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    anomalies = db.relationship("Anomaly", backref="project", lazy=True, cascade="all, delete-orphan")

class Anomaly(db.Model):
    __tablename__ = "anomalies"
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    anomaly_type = db.Column(db.String(50))
    severity_score = db.Column(db.Float, default=0.0)
    description = db.Column(db.Text)
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed = db.Column(db.Boolean, default=False, nullable=False)
    notes = db.Column(db.Text)