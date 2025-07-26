from flask import Flask
from app.database import db
from app.routes import main

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://duct_db_user:SXQ9iAKpluAXibt4xcxhakJk4uoQCFko@dpg-d2075pp5pdvs73c6q740-a.singapore-postgres.render.com/duct_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    app.register_blueprint(main)

    return app
