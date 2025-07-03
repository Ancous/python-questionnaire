"""
Документация модуля
"""

from werkzeug.security import generate_password_hash
from flask import Blueprint, flash, redirect, url_for, render_template, session

from app.form.register import RegistrationForm
from app.models import Session
from app.models.answered_questions import AnsweredQuestions
from app.models.user import Users

register_bp = Blueprint(
    "register",
    __name__,
    url_prefix="/register"
)


@register_bp.route('/', methods=['GET', 'POST'])
def register():
    """
    Документация функции
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        with Session() as se:
            if not Users.get_user(se, form.username.data.strip()):
                hashed_pw = generate_password_hash(form.password.data)
                user = Users.add_user(se, form.username.data.strip(), hashed_pw)
                count = AnsweredQuestions.get_numbers_count(se, user_id=user.id)
                session['number_questions_answered'] = 402 - count
                session['logged_in'] = True
                session['user_id'] = user.id
                session['username'] = user.username
                flash("Регистрация прошла успешно!", "register")
                return redirect(url_for('main.main'))

            flash('Пользователь уже существует.', "register")
            return redirect(url_for('register.register', form=form))

    return render_template('register.html', form=form)
