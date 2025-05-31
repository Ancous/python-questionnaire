"""
Документация модуля
"""

import markdown

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
            .filter(~Questions.id.in_(answered_ids))
            .order_by(func.random())
            .first()
        )
        question_obj = None
        if question_obj is None:
            message = "Вы знаете все ответы на вопросы. Вопросов для Вас больше нет."
            return render_template(
                'question.html',
                authorization=bool(session.get('logged_in')),
                result=None,
                text=None,
                message=message
            )

        html = markdown.markdown(
            question_obj.sub_question,
            extensions=['fenced_code']
        ) if question_obj.sub_question else None

    return render_template(
        'question.html',
        authorization=bool(session.get('logged_in')),
        result=question_obj,
        text=html,
        message=None
    )
