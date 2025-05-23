"""
Документация модуля
"""

from flask import Blueprint, render_template

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
    return render_template(template_name_or_list='answer_index.html')
