# app/seed.py (or routes/seed.py depending on your structure)
from flask import Blueprint
from .models import db, User

seed_bp = Blueprint('seed', __name__)

@seed_bp.route('/seed_user')
def seed_user():
    if not User.query.filter_by(username='admin').first():
        user = User(username='admin')
        user.set_password('admin123')  # hashed password
        db.session.add(user)
        db.session.commit()
        return "Dummy user created."
    return "User already exists."
