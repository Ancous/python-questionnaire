"""
Документация модуля
"""

from flask import render_template, Blueprint

from app.form.login import LoginForm

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
        # логика обработки данных для входа !!!

        return render_template(template_name_or_list='index.html')

    return render_template(template_name_or_list='login.html', form=form)
