"""
Документация модуля
"""

from flask import Blueprint, render_template

statistic_bp = Blueprint(
    "statistic",
    __name__,
    url_prefix="/statistic"
)


@statistic_bp.route("/", methods=["GET"])
def statistic():
    """
    Документация функции
    """
    return render_template(template_name_or_list='statistic_index.html')
