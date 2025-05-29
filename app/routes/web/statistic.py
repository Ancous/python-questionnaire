"""
Документация модуля
"""

from flask import Blueprint, render_template, session

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
    authorization = False
    if session.get('logged_in'):
        authorization = True
    return render_template(template_name_or_list='statistic.html', authorization=authorization)
