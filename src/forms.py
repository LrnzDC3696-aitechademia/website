from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from src.models import User

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

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if user is None:
            return

        raise ValidationError('Username is taken. Please thing for another one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user is None:
            return

        raise ValidationError('Email is taken. No alts allowed')

class LoginForms(FlaskForm):
    email = StringField('Email',
            validators=[DataRequired(), Email()])
    password = PasswordField('Password',
            validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

