"""
Документация модуля
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField(
        label='Имя пользователя',
        validators=[
            DataRequired(),
            Length(
                min=3,
                max=25
            )
        ]
    )
    password = PasswordField(
        label='Пароль',
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )
    confirm = PasswordField(
        label='Подтвердите пароль',
        validators=[
            DataRequired(),
            EqualTo(
                fieldname='password',
                message='Пароли должны совпадать.'
            )
        ]
    )
    submit = SubmitField('Зарегистрироваться')
