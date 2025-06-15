"""
Документация модуля
"""
import random

from flask import Blueprint, render_template, session, request, redirect, url_for
# from sqlalchemy import select, and_

from app.models import Session
from app.models.answered_questions import AnsweredQuestions
from app.models.question import Questions
from app.utils.processing_response_history import process_user_answer

question_bp = Blueprint(
    "question",
    __name__,
    url_prefix="/question"
)


# ALL_ID_QUESTION = 26


@question_bp.route("/", methods=["GET", "POST"])
def question():
    """
    pass
    """
    session['statistic'] = None
    session['question_all'] = None
    with Session() as se:
        if request.method == 'POST' and bool(session.get('logged_in')):
            if request.form.get('action'):
                process_user_answer(se, session.get("user_id"), session.get("question_id"), request.form.get('action'))

        answered_ids = AnsweredQuestions.get_numbers(se, session.get("user_id"))
        random_question_id = 0

        if answered_ids is None:
            random_question_id = random.randint(1, 200)
        else:
            available_numbers = list(set(range(1, 200)) - set(answered_ids))
            if available_numbers:
                random_question_id = random.choice(available_numbers)

        return redirect(url_for('question_question_id.question_question_id', question_id=random_question_id))
