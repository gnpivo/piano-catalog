import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize the modules
app = Flask(__name__)
db = SQLAlchemy()
db_url = os.environ.get("DATABASE_URL")

# Initialize the app for use with the database
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
db.init_app(app)

# Import the blueprint
from app import catalog

# Register the blueprint
app.register_blueprint(catalog.bp)

# Create the tables if they do not exist yet
with app.app_context():
    db.create_all()

# Add the URL rule for the "catalog" blueprint
app.add_url_rule("/", endpoint="index")
