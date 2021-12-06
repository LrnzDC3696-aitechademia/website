from flask import render_template, url_for, flash, redirect, request
from src import app, db, bcrypt
from src.forms import RegistrationForms, LoginForms
from src.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

posts = [
    {
        'author': 'Lorenzo',
        'title' : 'Blog Post 1',
        'content' : 'First post content',
        'date_posted':'June 22 2021'
    },
    {
        'author': 'Jane Doe',
        'title' : 'Blog Post 2',
        'content' : 'Second post content',
        'date_posted':'April 20, 2021'
    }
]

@app.route('/')
def index():
    return render_template('index.html', posts=posts)

@app.route('/')
def about():
    return render_template('index.html', posts=posts)

@app.route('/register/', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegistrationForms()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data) \
            .decode('utf-8')
        user = User(username=form.username.data, email=form.email.data,
            password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login/', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForms()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful, Please check username and password',
               'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Account')
