"""
Документация модуля
"""

from typing import cast
from flask import Blueprint, render_template, session, request

from app.models import Session
from app.models.question import Questions
from app.utils.processing_response_history import process_user_answer
from app.utils.processing_statistic_data import statistic_data

statistic_bp = Blueprint(
    "statistic",
    __name__,
    url_prefix="/statistic"
)


@statistic_bp.route("/", methods=["GET", "POST"])
def statistic():
    """
    Документация функции
    """
    session['statistic'] = None
    session['question_all'] = None
    with Session() as se:
        if request.method == 'POST' and request.form.get('action'):
            process_user_answer(
                se,
                user_id=cast(int, session.get("user_id")),
                question_id=cast(int, session.get("question_id")),
                action=cast(str, request.form.get('action')),
                statistic_questionall=True
            )

        user_statistic_obj = Questions.get_questions_grouped_by_answer_option(se, session.get('user_id'))
        session_data = statistic_data(user_statistic_obj)
        return render_template('statistic.html', data=session_data)
