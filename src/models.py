from datetime import datetime

from flask import current_app
from flask_login import UserMixin
from flask_sqlalchemy import event
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from src import bcrypt, db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


user_role = db.Table(
    "user_role",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id")),
)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpeg")
    password = db.Column(db.String(60), nullable=False)

    roles = db.relationship(
        "Role", secondary=user_role, backref=db.backref("users", lazy="dynamic")
    )

    posts = db.relationship("Post", backref="author", lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    @property
    def is_admin(self):
        return self.is_authenticated and self.has_role("admin")

    def has_role(self, role):
        return role.lower() in {r.name.lower() for r in self.roles}

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except KeyError:
            return None

        return User.query.get(user_id)

    def __repr__(self):
        return f"User({self.username=}, {self.email=}, {self.image_file=})"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Post({self.title=}, {self.date_posted=})"


class Role(db.Model):
    __tablename__ = "role"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    description = db.Column(db.String(169), nullable=False)

    def __repr__(self):
        return f"Role({self.name=})"


@event.listens_for(Role.__table__, "after_create", once=True)
def add_initial_role(*args, **kwargs):
    db.session.add(Role(name="admin", description="Administrator"))
    db.session.add(Role(name="verified", description="Verified user"))
    db.session.commit()


@event.listens_for(User.__table__, "after_create", once=True)
def add_initial_user(*args, **kwargs):
    password = bcrypt.generate_password_hash(
        current_app.config["MAIN_ADMIN_PASSWORD"]
    ).decode("utf-8")

    user = User(
        username=current_app.config["MAIN_ADMIN_USERNAME"],
        email=current_app.config["MAIN_ADMIN_EMAIL"],
        password=password,
    )

    db.session.add(user)
    db.session.commit()


@event.listens_for(user_role, "after_create", once=True)
def add_initial_user_role(*args, **kwargs):
    admin_role = Role.query.filter_by(name="admin").first()

    user = User.query.filter_by(email=current_app.config["MAIN_ADMIN_EMAIL"]).first()
    user.roles.append(admin_role)
    db.session.commit()
