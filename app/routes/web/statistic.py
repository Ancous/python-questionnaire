"""
Модуль реализует обработку маршрута для отображения статистики пользователя.
"""

from typing import cast
from flask import Blueprint, render_template, session, request
from flask.typing import ResponseReturnValue

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
def statistic() -> ResponseReturnValue:
    """
    Обрабатывает GET и POST запросы для отображения статистики пользователя и обработки ответов.

    Return:
    html (ResponseReturnValue): HTML-страница со статистикой пользователя
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

        user_statistic_obj = Questions.get_questions_grouped_by_answer_option(se, cast(int, session.get("user_id")))
        user_statistic_tuples = [tuple(row) for row in user_statistic_obj]
        session_data = statistic_data(user_statistic_tuples)
        return render_template('statistic.html', data=session_data)
