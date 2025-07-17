"""
Модуль с формой входа пользователя.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

from app.form.custom_validation import CheckRecord


class LoginForm(FlaskForm):
    """
    Форма для входа пользователя.

    Аргументы:
    username (StringField): поле для ввода имени пользователя
    password (PasswordField): поле для ввода пароля
    submit (SubmitField): кнопка отправки формы
    """

    username: StringField = StringField(
        label="Username",
        validators=[
            CheckRecord(message="Поле не должно быть пустым"),
        ],
    )
    password: PasswordField = PasswordField(
        label="Password",
        validators=[
            CheckRecord(message="Поле не должно быть пустым"),
        ],
    )
    submit: SubmitField = SubmitField("Вход")
