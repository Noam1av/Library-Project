from flask import Flask
from models import db
from models.admin import Admin  # Adjusted import to match app.py
from app import app  # Updated to match the actual Flask app instance


with app.app_context():


    email = "29noam@gmail.com"
    password = "290106na"
    new_admin = Admin(email=email, password=password)
    db.session.add(new_admin)
    db.session.commit()

