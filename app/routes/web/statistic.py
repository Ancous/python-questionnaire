"""
Документация модуля
"""

from flask import Blueprint, render_template, session

from app.models import Session
from app.models.user_statistic import UserStatistic
from app.utils.processing_statistic_data import statistic_data

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
    with Session() as se:
        user_statistic_obj = UserStatistic.all_statistic_for_user(se, session.get('user_id'))
        data = statistic_data(user_statistic_obj)

    return render_template(
        template_name_or_list='statistic.html',
        data=data
    )
