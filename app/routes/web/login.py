"""
Документация модуля
"""

from flask import render_template, Blueprint, redirect, session, url_for, flash
from werkzeug.security import check_password_hash

from app.config.config import NUMBER_OF_QUESTIONS
from app.form.login import LoginForm
from app.models import Session
from app.models.answered_questions import AnsweredQuestions
from app.models.user import Users

login_bp = Blueprint(
    "login",
    __name__,
    url_prefix="/login"
)


@login_bp.route('/', methods=['GET', "POST"])
def login():
    """
    Документация функции
    """
    form = LoginForm()
    if form.validate_on_submit():
        with Session() as se:
            user = se.query(Users).filter_by(username=form.username.data).first()
            if user and check_password_hash(user.password, form.password.data):
                count = AnsweredQuestions.get_numbers_count(se, user_id=user.id)
                session['number_questions_answered'] = NUMBER_OF_QUESTIONS - count
                session['logged_in'] = True
                session['user_id'] = user.id
                session['username'] = user.username
                flash("Вы успешно вошли в систему.", "login")
                return redirect(url_for('main.main'))

            flash("Вы неверно ввели логин или пароль", "login")
            return render_template('login.html', form=form)

    return render_template('login.html', form=form)
