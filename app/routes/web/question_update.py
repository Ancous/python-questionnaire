"""
Модуль реализует обработку маршрута для сброса прогресса пользователя по вопросам.
"""

from flask import Blueprint, flash, redirect, url_for, session
from flask.typing import ResponseReturnValue

from app.models import Session
from app.models.answered_questions import AnsweredQuestions
from app.models.user_statistic import UserStatistic

question_update_bp = Blueprint(
    "question_update",
    __name__,
    url_prefix="/question_update"
)


@question_update_bp.route("/", methods=["GET"])
def question_update() -> ResponseReturnValue:
    """
    Обрабатывает GET-запрос для сброса прогресса пользователя по вопросам.

    Return:
    redirect (ResponseReturnValue): перенаправление на главную страницу после сброса
    """
    with Session() as se:
        AnsweredQuestions.clear_answered_questions(se, session.get("user_id"))
        UserStatistic.delete_answer_for_user_id(se, session.get("user_id"))
        session['number_questions_answered'] = 200

    flash("Вопросы обновлены", "update")
    return redirect(url_for('main.main'))
