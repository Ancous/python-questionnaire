"""
Модуль реализует обработку маршрута для регистрации пользователя.
"""

from typing import cast
from werkzeug.security import generate_password_hash
from flask import Blueprint, flash, redirect, url_for, render_template, session
from flask.typing import ResponseReturnValue

from app.config.config import NUMBER_OF_QUESTIONS
from app.form.register import RegistrationForm
from app.models import Session
from app.models.answered_questions import AnsweredQuestions
from app.models.user import Users

register_bp = Blueprint("register", __name__, url_prefix="/register")


@register_bp.route("/", methods=["GET", "POST"])
def register() -> ResponseReturnValue:
    """
    Обрабатывает GET и POST запросы для регистрации пользователя.

    Return:
    html (ResponseReturnValue): HTML-страница с формой регистрации или перенаправление после успешной регистрации
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        with Session() as se:
            username = cast(str, form.username.data)
            password = cast(str, form.password.data)
            if not Users.get_user(se, username.strip()):
                hashed_pw = generate_password_hash(password)
                user = Users.add_user(se, username.strip(), hashed_pw)
                count = AnsweredQuestions.get_numbers_count(se, user_id=user.id)
                session["number_questions_answered"] = NUMBER_OF_QUESTIONS - count
                session["logged_in"] = True
                session["user_id"] = user.id
                session["username"] = user.username
                flash("Регистрация прошла успешно!", "register")
                return redirect(url_for("main.main"))

            flash("Пользователь уже существует.", "register")
            return redirect(url_for("register.register", form=form))

    return render_template("register.html", form=form)
