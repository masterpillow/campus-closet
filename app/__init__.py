# __init__.py
# This initializes the Flask application, its extensions, and blueprints
# It defines the create_app() function used to configure and return the app instance

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Initialize SQLAlchemy for ORM/database support 
db = SQLAlchemy()

# Set up Flask-Login to manage user authentication and sessions 
login_manager = LoginManager()
login_manager.login_view = 'main.login'

# Factory function to create and configure a Flask app instance 
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from . import routes
    app.register_blueprint(routes.bp)

    with app.app_context():
      #  db.drop_all() #
        db.create_all()

    return app
