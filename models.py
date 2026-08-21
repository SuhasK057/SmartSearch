from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)[cite: 3]
    password_hash = db.Column(db.String(256), nullable=False)[cite: 3]
    user_type = db.Column(db.String(50))  # e.g., student, job_seeker, senior citizen[cite: 3]
    
    # Relationships
    saved_jobs = db.relationship('SavedJob', backref='user', lazy=True)
    preferences = db.relationship('UserPreference', backref='user', uselist=False, lazy=True)

class SavedJob(db.Model):
    __tablename__ = 'saved_jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)[cite: 3]
    title = db.Column(db.String(200))[cite: 3]
    company = db.Column(db.String(200))[cite: 3]
    link = db.Column(db.Text)[cite: 3]
    location = db.Column(db.String(100))[cite: 3]
    saved_at = db.Column(db.DateTime, default=datetime.utcnow)[cite: 3]

class UserPreference(db.Model):
    __tablename__ = 'user_preferences'
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)[cite: 3]
    preferred_categories = db.Column(db.Text)  # Comma-separated or JSON list of genres[cite: 3]