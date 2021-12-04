from flask import Flask, render_template, url_for
#  from .forms import RegistrationForms, LoginForms


app = Flask(__name__)
app.config['SECRET_KEY'] = 'a very secret key that you don\'t know'


@app.route('/')
def index():
    return render_template('index.html')

#  @app.route('/register/')
#  def register():
#      form = RegistrationForms()
#      return render_template('register.html', title='Register', form=form)
#
#  @app.route('/login/')
#  def login():
#      form = LoginForms()
#      return render_template('login.html', title='Login', form=form)


