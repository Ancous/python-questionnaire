"""
Документация модуля
"""

from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, PasswordField, SubmitField


class LoginForm(FlaskForm):
    username = StringField(
        label='Username',
        validators=[
            DataRequired()
        ]
    )
    password = PasswordField(
        label='Password',
        validators=[
            DataRequired()
        ]
    )
    submit = SubmitField('Войти')
