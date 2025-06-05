"""
Документация модуля
"""

from flask import Blueprint, flash, redirect, url_for, session

from app.models import Session
from app.models.answered_questions import AnsweredQuestions

question_update_bp = Blueprint(
    "question_update",
    __name__,
    url_prefix="/question_update"
)


@question_update_bp.route("/", methods=["GET"])
def question_update():
    """
    Документация функции
    """
    with Session() as se:
        AnsweredQuestions.clear_answered_questions(se, session.get("user_id"))

    flash("Вопросы обновлены", "update")
    return redirect(url_for('main.main'))
