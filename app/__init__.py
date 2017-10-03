from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

from config import app_config


db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_name):

    # Initialize application object
    app = Flask('app', template_folder='templates', instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    # Initialize use of database
    db.init_app(app)    

    # Create object for database migrations
    # To make a migration, type: `flask db migrate; flask db upgrade`
    migrate = Migrate(app, db)

    # Initialize login manager
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page"
    login_manager.login_view = "auth.login" # not yet created

    # Initialize Bootstrap utility
    Bootstrap(app)

    from app import models

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)


    return app