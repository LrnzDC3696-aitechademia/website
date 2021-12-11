import os
import secrets

from PIL import Image
from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from src import app, bcrypt, db
from src.forms import LoginForm, RegistrationForm, UpdateAccountForm
from src.models import Post, User


posts = [
    {
        "author": "Lorenzo",
        "title": "Blog Post 1",
        "content": "First post content",
        "date_posted": "June 22 2021",
    },
    {
        "author": "Jane Doe",
        "title": "Blog Post 2",
        "content": "Second post content",
        "date_posted": "April 20, 2021",
    },
]


@app.route("/")
def index():
    return render_template("index.html", posts=posts)


@app.route("/about/")
def about():
    return render_template("index.html", posts=posts)


@app.route("/register/", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = RegistrationForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        db.session.add(user)
        db.session.commit()

        flash(f"Account created for {form.username.data}!", "success")
        return redirect(url_for("index"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("index"))
        else:
            flash("Login Unsuccessful, Please check username and password", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for("index"))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/profile_pics", picture_fn)

    OUTPUT_SIZE = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(OUTPUT_SIZE)
    i.save(picture_path)

    return picture_fn


def delete_picture(picture_fn):
    picture_path = os.path.join(app.root_path, "static/profile_pics", picture_fn)
    os.remove(picture_path)


@app.route("/account/", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            delete_picture(current_user.image_file)
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for("static", filename=f"profile_pics/{ current_user.image_file }")
    return render_template(
        "account.html", title="Account", image_file=image_file, form=form
    )
