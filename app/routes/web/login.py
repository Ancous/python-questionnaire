"""
Документация модуля
"""

from flask import render_template, Blueprint, redirect, session, url_for
from werkzeug.security import check_password_hash

from app.form.login import LoginForm
from app.models import Session
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
                session['logged_in'] = True
                session['username'] = user.username
                session['user_id'] = user.id
                return redirect(url_for('main.main'))

    return render_template(template_name_or_list='login.html', form=form)
