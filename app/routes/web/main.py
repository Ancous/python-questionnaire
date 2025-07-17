"""
Модуль реализует основной маршрут отображения главной страницы.
"""

from flask import Blueprint, render_template
from flask.typing import ResponseReturnValue

main_bp = Blueprint("main", __name__, url_prefix="/")


@main_bp.route("/", methods=["GET"])
def main() -> ResponseReturnValue:
    """
    Обрабатывает GET-запрос для отображения главной страницы.

    Return:
    html (ResponseReturnValue): HTML-страница с главной страницей
    """
    return render_template("index.html")
