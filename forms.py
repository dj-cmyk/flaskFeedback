from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email
import email_validator

class RegisterUserForm(FlaskForm):
    '''docstring'''

    username = StringField('UserName', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    email = StringField('Email Address', validators=[InputRequired(), Email()])
    first_name = StringField('First Name', validators=[InputRequired()])
    last_name = StringField('Last Name', validators=[InputRequired()])


class LoginForm(FlaskForm):
    '''docstring'''

    username = StringField('UserName', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])


class FeedbackForm(FlaskForm):
    '''docstring'''

    title = StringField('Title', validators=[InputRequired()])
    content = StringField('Content', validators=[InputRequired()])