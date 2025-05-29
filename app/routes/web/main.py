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
    authorization = False
    if session.get('logged_in'):
        authorization = True
    return render_template(template_name_or_list='index.html', authorization=authorization)
