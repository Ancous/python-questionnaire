"""
Документация модуля
"""

from flask import Blueprint, render_template

questions_bp = Blueprint(
    "questions",
    __name__,
    url_prefix="/questions"
)


@questions_bp.route("/", methods=["GET"])
def questions():
    """
    Документация функции
    """
    return render_template(template_name_or_list='question_index.html')
