from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForms(FlaskForm):
    username = StringField('Username',
            validators=[DataRequired(), Length(min=3, max=30)])

    email = StringField('Email',
            validators=[DataRequired(), Email()])

    password = PasswordField('Password',
            validators=[DataRequired()])

    confirm_password = PasswordField('Confirm Password',
            validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Sign Up')

class LoginForms(FlaskForm):
    email = StringField('Email',
            validators=[DataRequired(), Email()])
    password = PasswordField('Password',
            validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

