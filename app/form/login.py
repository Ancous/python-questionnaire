"""
Документация модуля
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

from app.form.custom_validation import CheckRecord


class LoginForm(FlaskForm):
    username = StringField(
        label='Username',
        validators=[
            CheckRecord(
                message="Поле не должно быть пустым"
            ),
        ]
    )
    password = PasswordField(
        label='Password',
        validators=[
            CheckRecord(
                message="Поле не должно быть пустым"
            ),
        ]
    )
    submit = SubmitField('Войти')
