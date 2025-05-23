"""
Документация модуля
"""

from flask import Blueprint, render_template

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
    return render_template(template_name_or_list='question_index.html')
