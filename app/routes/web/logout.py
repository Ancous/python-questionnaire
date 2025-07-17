"""
Модуль реализует обработку маршрута выхода пользователя из системы.
"""

from flask import session, Blueprint, redirect, url_for, flash
from flask.typing import ResponseReturnValue

logout_bp = Blueprint("logout", __name__, url_prefix="/logout")


@logout_bp.route("/", methods=["GET"])
def logout() -> ResponseReturnValue:
    """
    Обрабатывает GET-запрос для выхода пользователя из системы.

    Return:
    redirect (ResponseReturnValue): перенаправление на главную страницу после выхода
    """
    session.clear()
    flash("Вы успешно вышли из системы.", "logout")
    return redirect(url_for("main.main"))
