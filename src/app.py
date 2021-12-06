from flask import Flask, render_template, url_for, flash, redirect
from src.forms import RegistrationForms, LoginForms

import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

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


