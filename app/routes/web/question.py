"""
Документация модуля
"""

from flask import Blueprint, render_template, session, request
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
    with Session() as se:
        if request.method == 'POST' and bool(session.get('logged_in')):
            if request.form.get('action'):
                process_user_answer(se, session.get("user_id"), session.get("question_id"), request.form.get('action'))

        answered_ids = AnsweredQuestions.get_numbers(se, session.get("user_id"))
        question_obj = Questions.get_random_unanswered_question(se, answered_ids)

        # global ALL_ID_QUESTION
        # stmt = select(Questions).where(and_(Questions.id == ALL_ID_QUESTION))
        # question_obj = se.execute(stmt).scalars().first()
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
