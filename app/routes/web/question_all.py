"""
Документация модуля
"""

from flask import Blueprint, render_template, session

from app.models import Session
from app.models.question import Questions


def create_question_all_bp(cache):
    """
    Документация функции
    """
    question_all_bp = Blueprint(
        'question_all',
        __name__,
        url_prefix="/question/all"
    )

    @question_all_bp.route('/', methods=["GET"])
    @cache.cached(timeout=3600)
    def question_all():
        """
        Документация функции
        """
        session['statistic'] = None
        session['question_all'] = None
        with Session() as se:
            question_obj = Questions.all_questions(se)
            session['question_all'] = [
                {
                    "question_id": q.id,
                    "question": q.question,
                    "sub_question": q.sub_question
                }
                for q in question_obj
            ]
        return render_template('question_all.html')

    return question_all_bp
