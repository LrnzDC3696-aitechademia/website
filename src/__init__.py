from flask import Flask, url_for
from flask_admin import Admin
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
admin = Admin(name="Aitechademia")


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from src.errors.handlers import errors
    from src.main.routes import main
    from src.posts.routes import posts
    from src.tools.routes import tools
    from src.users.routes import users

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(tools)

    from src.admin_stuff.views import MyAdminIndexView, MyModelView
    from src.models import Post, Role, User

    admin.init_app(app, index_view=MyAdminIndexView(), url="/")
    admin.add_view(MyModelView(Role, db.session))
    admin.add_view(MyModelView(User, db.session))
    admin.add_view(MyModelView(Post, db.session))

    with app.app_context():
        db.create_all()

    return app
