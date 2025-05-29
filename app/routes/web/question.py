"""
Документация модуля
"""

from flask import Blueprint, render_template, session

question_bp = Blueprint(
    "question",
    __name__,
    url_prefix="/question"
)


@question_bp.route("/", methods=["GET"])
def question():
    """
    Документация функции
    """
    authorization = False
    if session.get('logged_in'):
        authorization = True
    return render_template(template_name_or_list='question.html', authorization=authorization)
