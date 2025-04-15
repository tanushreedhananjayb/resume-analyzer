# app/database.py

from app import db
from app.models import User, ResumeData

def create_database(app):
    with app.app_context():
        db.create_all()
        print("✅ Database tables created successfully.")
