from flask import Flask
from flask_migrate import Migrate
from .database import db, init_app
from .routes import main as main_blueprint
from .models import User
from .seed import seed_bp

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'

    # Initialize database and migrations
    init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(main_blueprint)
    app.register_blueprint(seed_bp)

    with app.app_context():
        db.create_all()

        # Add dummy admin user if not already present
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()

    return app
