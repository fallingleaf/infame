from itertools import imap

from flask import current_app
from flask_wtf import FlaskForm

from wtforms import TextField, PasswordField, BooleanField
from wtforms.validators import Required, Email, ValidationError

from aura.database.model import User


def _validate_password(passwd):
    min_length = current_app.config['MIN_PASSWD_LENGTH']
    if len(passwd) < min_length:
        return False, 'Your password must contain at least %s characters.' % min_length
    if not any(imap(str.isdigit, str(passwd))) or not any(imap(str.isalpha, str(passwd))):
        return False, 'Your password must have at least 1 number and 1 letter.'
    return True, ''


class LoginForm(FlaskForm):
    email = TextField('Email Address', [Email(),
                        Required(message='Email is required')])
    password = PasswordField('Password', [Required(message='Password is required')])
    remember = BooleanField('Remember me', [])


class SignupForm(FlaskForm):
    username = TextField('Username', [Required(message='Please enter username')])
    email = TextField('Email Address', [Email(), Required(message='Email is required')])
    password = PasswordField('Password', [Required(message='Password is required')])

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError("Email's already in use")

    def validate_password(self, field):
        valid, msg = _validate_password(field.data)
        if not valid:
            raise ValidationError(msg)
