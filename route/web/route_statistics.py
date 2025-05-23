"""
Документация модуля
"""

from flask import Blueprint, render_template

statistics_bp = Blueprint(
    "statistics",
    __name__,
    url_prefix="/statistics"
)


@statistics_bp.route("/", methods=["GET"])
def statistics():
    """
    Документация функции
    """
    return render_template(template_name_or_list='statistics_index.html')
