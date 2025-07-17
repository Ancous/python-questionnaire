"""
Модуль реализует обработку маршрута для вывода случайного вопроса пользователю.
"""

import random
from typing import cast

from flask import Blueprint, session, request, redirect, url_for
from flask.typing import ResponseReturnValue

from app.config.config import NUMBER_OF_QUESTIONS
from app.models import Session
from app.models.answered_questions import AnsweredQuestions
from app.utils.processing_response_history import process_user_answer

question_bp = Blueprint("question", __name__, url_prefix="/question")


@question_bp.route("/", methods=["GET", "POST"])
def question() -> ResponseReturnValue:
    """
    Обрабатывает GET и POST запросы для вывода случайного вопроса пользователю и обработки ответа.

    Return:
    redirect (ResponseReturnValue): перенаправление на страницу с вопросом
    """
    session["statistic"] = None
    session["question_all"] = None
    with Session() as se:
        if request.method == "POST" and bool(session.get("logged_in")):
            if request.form.get("action"):
                process_user_answer(
                    se,
                    user_id=cast(int, session.get("user_id")),
                    question_id=cast(int, session.get("question_id")),
                    action=cast(str, request.form.get("action")),
                    statistic_questionall=False,
                )

        answered_ids = AnsweredQuestions.get_numbers(
            se, cast(int, session.get("user_id"))
        )
        random_question_id = 0

        if answered_ids is None:
            random_question_id = random.randint(1, NUMBER_OF_QUESTIONS + 1)
        else:
            available_numbers = list(
                set(range(1, NUMBER_OF_QUESTIONS + 1)) - set(answered_ids)
            )
            if available_numbers:
                random_question_id = random.choice(available_numbers)

        return redirect(url_for("question_id.question_id", id=random_question_id))
