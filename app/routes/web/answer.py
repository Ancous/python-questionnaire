"""
Документация модуля
"""

from flask import Blueprint, render_template, session

answer_bp = Blueprint(
    "answer",
    __name__,
    url_prefix="/answer"
)


@answer_bp.route("/", methods=["GET"])
def answer():
    """
    Документация функции
    """
    authorization = False
    if session.get('logged_in'):
        authorization = True
    return render_template(template_name_or_list='answer.html', authorization=authorization)
