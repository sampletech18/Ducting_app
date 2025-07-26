from flask import Flask
from flask_migrate import Migrate
from .database import db, init_app
from .routes import main as main_blueprint
from .models import User
from .seed import seed_bp
from sqlalchemy import text  # ✅ add this

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'

    init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(main_blueprint)
    app.register_blueprint(seed_bp)

    with app.app_context():
        db.create_all()

        # ✅ Fix missing gst_number column if not exists
        try:
            db.session.execute(text("ALTER TABLE vendor ADD COLUMN gst_number VARCHAR(50)"))
            db.session.commit()
            print("✅ Added gst_number column.")
        except Exception as e:
            print("ℹ️ Column may already exist:", e)

        # Dummy user
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()

    return app
