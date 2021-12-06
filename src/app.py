from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from src.forms import RegistrationForms, LoginForms
from datetime import datetime

import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpeg')
    password = db.Column(db.String(60), nullable=False)

    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User({self.username=}, {self.email=}, {self.image_file=})"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post({self.title=}, {self.date_posted=})"

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
    form = RegistrationForms()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login/', methods=['GET','POST'])
def login():
    form = LoginForms()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been loggen in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful, Please check username and password',
               'danger')
    return render_template('login.html', title='Login', form=form)


