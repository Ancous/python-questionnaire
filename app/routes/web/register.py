"""
Документация модуля
"""

from werkzeug.security import generate_password_hash
from flask import Blueprint, flash, redirect, url_for, render_template, session

from app.form.register import RegistrationForm
from app.models import Session
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
            if se.query(Users).filter_by(username=form.username.data.strip()).first():
                flash('Пользователь уже существует.')
                form.password.data = form.password.data
                return render_template(template_name_or_list='register.html', form=form)

            hashed_pw = generate_password_hash(form.password.data)
            user = Users(username=form.username.data.strip(), password=hashed_pw)
            se.add(user)
            se.commit()
            flash("Регистрация прошла успешно!", "register")
            session['logged_in'] = True
            session['username'] = user.username
        return redirect(url_for('main.main'))

    return render_template(template_name_or_list='register.html', form=form)
