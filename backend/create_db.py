# create_db.py
from main import app, db

with app.app_context():
    db.create_all()
