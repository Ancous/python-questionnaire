"""
Документация модуля
"""

from flask import Blueprint, render_template, session

main_bp = Blueprint(
    "main",
    __name__,
    url_prefix="/"
)


@main_bp.route("/", methods=["GET"])
def main():
    """
    Документация функции
    """
    return render_template(
        template_name_or_list='index.html',
        authorization=bool(session.get('logged_in'))
    )
