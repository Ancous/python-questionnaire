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

ALL_ID_QUESTION = 26


@question_bp.route("/", methods=["GET"])
def question():
    """
    Документация функции
    """
    answered_ids = [4, 6, 10]  # запрос на получение id отвеченных вопросов у пользователя
    # global ALL_ID_QUESTION
    with Session() as se:
        question_obj = (
            se.query(Questions)
            # .filter(Questions.id == ALL_ID_QUESTION)
            .filter(~Questions.id.in_(answered_ids))
            .order_by(func.random())
            .first()
        )

        # ALL_ID_QUESTION += 1

        if question_obj is None:
            message = "Вы знаете все ответы на вопросы. Вопросов для Вас больше нет."
            return render_template(
                'question.html',
                authorization=bool(session.get('logged_in')),
                question=None,
                sub_question=None,
                message=message
            )

        session['question_id'] = question_obj.id
        session['question'] = question_obj.question
        session['sub_question'] = question_obj.sub_question

    return render_template(
        'question.html',
        authorization=bool(session.get('logged_in')),
        question_id=session.get("question_id"),
        question=session.get("question"),
        sub_question=session.get("sub_question"),
        message=None
    )
