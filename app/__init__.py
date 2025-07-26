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

        # ✅ Safely patch missing Vendor table columns
        alter_statements = [
            "ALTER TABLE vendor ADD COLUMN IF NOT EXISTS gst_number VARCHAR(50)",
            "ALTER TABLE vendor ADD COLUMN IF NOT EXISTS address VARCHAR(250)",
            "ALTER TABLE vendor ADD COLUMN IF NOT EXISTS contact_person VARCHAR(100)",
            "ALTER TABLE vendor ADD COLUMN IF NOT EXISTS contact_email VARCHAR(100)",
            "ALTER TABLE vendor ADD COLUMN IF NOT EXISTS contact_phone VARCHAR(20)",
            "ALTER TABLE vendor ADD COLUMN IF NOT EXISTS bank_name VARCHAR(100)",
            "ALTER TABLE vendor ADD COLUMN IF NOT EXISTS bank_account VARCHAR(100)",
            "ALTER TABLE vendor ADD COLUMN IF NOT EXISTS ifsc VARCHAR(20)"
        ]
        for stmt in alter_statements:
            try:
                db.session.execute(text(stmt))
            except Exception as e:
                print(f"⚠️ Could not apply: {stmt}\n{e}")

        db.session.commit()
        print("✅ Vendor table columns verified/added.")

        # ✅ Add dummy admin user if not present
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Dummy admin user created.")

    return app
