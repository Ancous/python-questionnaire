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
        answer_obj = Answers.answer_by_question_id(se, session["question_id"])
    return render_template(
        template_name_or_list='answer.html',
        authorization=bool(session.get('logged_in')),
        question=session.get("question"),
        sub_question=session.get("sub_question"),
        question_id=session.get("question_id"),
        sub_answer=answer_obj.answer
    )
