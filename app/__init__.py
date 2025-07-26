from flask import Flask
from flask_migrate import Migrate  # ✅ Add this
from .database import db, init_app
from .routes import main as main_blueprint
from .models import User
from .seed import seed_bp

migrate = Migrate()  # ✅ Add this line

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'

    init_app(app)
    migrate.init_app(app, db)  # ✅ This activates migrations

    app.register_blueprint(main_blueprint)
    app.register_blueprint(seed_bp)

    with app.app_context():
        db.create_all()

        # Dummy user: admin / admin123
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()

    return app
