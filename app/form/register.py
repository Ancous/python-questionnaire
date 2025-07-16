"""
Модуль содержит форму регистрации пользователя для веб-приложения на Flask.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import EqualTo

from app.form.custom_validation import CustomLength, CheckRecord


class RegistrationForm(FlaskForm):
    """
    Форма для регистрации нового пользователя.

    Arguments:
    username (StringField): Поле для ввода имени пользователя с валидацией.
    password (PasswordField): Поле для ввода пароля с валидацией.
    confirm (PasswordField): Поле для подтверждения пароля с валидацией.
    submit (SubmitField): Кнопка отправки формы.
    """
    username: StringField = StringField(
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
    password: PasswordField = PasswordField(
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
    confirm: PasswordField = PasswordField(
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
    submit: SubmitField = SubmitField('Зарегистрироваться')
