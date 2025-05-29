"""
Документация модуля
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import EqualTo

from app.form.custom_validation import CustomLength, CheckRecord


class RegistrationForm(FlaskForm):
    username = StringField(
        label='Имя пользователя',
        validators=[
            CheckRecord(
                message="Поле не должно быть пустым или состоять только из пробелов"
            ),
            CustomLength(
                min_text=3,
                max_text=25,
                message="Имя пользователя должен быть от 3 до 25 символов"
            )
        ]
    )
    password = PasswordField(
        label='Пароль',
        validators=[
            CheckRecord(
                message="Поле не должно быть пустым или состоять только из пробелов"
            ),
            CustomLength(
                min_text=3,
                message="Пароль должен быть от 3 символов"
            )
        ]
    )
    confirm = PasswordField(
        label='Подтвердите пароль',
        validators=[
            CheckRecord(
                message="Поле не должно быть пустым или состоять только из пробелов"
            ),
            EqualTo(
                fieldname='password',
                message='Пароли должны совпадать.'
            )
        ]
    )
    submit = SubmitField('Зарегистрироваться')
