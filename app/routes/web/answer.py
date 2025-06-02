"""
Документация модуля
"""

from flask import Blueprint, render_template, session

from app.models import Session
from app.models.answer import Answers

answer_bp = Blueprint(
    "answer",
    __name__,
    url_prefix="/answer"
)


@answer_bp.route("/", methods=["GET"])
def answer():
    """
    Документация функции
    """
    with Session() as se:
        answer_obj = (
            se.query(Answers)
            .filter(Answers.question_id == session["question"])
            .first()
        )

    return render_template(
        template_name_or_list='answer.html',
        authorization=bool(session.get('logged_in')),
        sub_answer=answer_obj.answer
    )
