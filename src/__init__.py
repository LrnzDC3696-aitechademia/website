from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

from src.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    for obj in (db, bcrypt, login_manager, mail):
        obj.init_app(app)

    from src.users.routes import users
    from src.posts.routes import posts
    from src.main.routes import main

    for blueprint in (users, posts, main):
        app.register_blueprint(blueprint)

    return app
