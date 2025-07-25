from flask import Flask
from database import db
from models import *
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://duct_db_user:SXQ9iAKpluAXibt4xcxhakJk4uoQCFko@dpg-d2075pp5pdvs73c6q740-a.singapore-postgres.render.com/duct_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'secret123'

db.init_app(app)
migrate = Migrate(app, db)

from routes import *

if __name__ == "__main__":
    app.run(debug=True)
