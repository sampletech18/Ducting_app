from flask import Flask
from flask_migrate import Migrate
from .database import db, init_app
from .routes import main as main_blueprint
from .models import User
from .seed import seed_bp
from sqlalchemy import text

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

        # ✅ Fix: Add any missing columns to 'vendor'
        try:
            db.session.execute(text("ALTER TABLE vendor ADD COLUMN IF NOT EXISTS gst_number VARCHAR(50)"))
            db.session.execute(text("ALTER TABLE vendor ADD COLUMN IF NOT EXISTS address TEXT"))
            db.session.execute(text("ALTER TABLE vendor ADD COLUMN IF NOT EXISTS email VARCHAR(120)"))
            db.session.execute(text("ALTER TABLE vendor ADD COLUMN IF NOT EXISTS phone VARCHAR(20)"))
            db.session.commit()
            print("✅ Ensured all expected vendor columns exist.")
        except Exception as e:
            print("⚠️ Column patching error:", e)

        # ✅ Admin account creation (first-time only)
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created.")

    return app
