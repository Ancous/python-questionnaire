"""
Документация модуля
"""

from flask import Blueprint, render_template, session
from sqlalchemy import func

from app.models import Session
from app.models.question import Questions

question_bp = Blueprint(
    "question",
    __name__,
    url_prefix="/question"
)

ALL_ID_QUESTION = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # все id вопросов


@question_bp.route("/", methods=["GET"])
def question():
    """
    Документация функции
    """
    answered_ids = [4, 6, 10]  # запрос на получение id отвеченных вопросов у пользователя

    with Session() as se:
        question_obj = (
            se.query(Questions)
            # .filter(Questions.id == 96)
            .filter(~Questions.id.in_(answered_ids))
            .order_by(func.random())
            .first()
        )
        if question_obj is None:
            message = "Вы знаете все ответы на вопросы. Вопросов для Вас больше нет."
            return render_template(
                'question.html',
                authorization=bool(session.get('logged_in')),
                question=None,
                sub_question=None,
                message=message
            )

        session['question'] = question_obj.id

    return render_template(
        'question.html',
        authorization=bool(session.get('logged_in')),
        question=question_obj,
        sub_question=question_obj.sub_question,
        message=None
    )
