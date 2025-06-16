"""
Документация модуля
"""
import time
from urllib.parse import urlparse

from flask import Blueprint, render_template, session, request

from app.models import Session
from app.models.answer import Answers
from app.models.question import Questions


def create_answer_bp(cache):
    """
    Документация функции
    """
    answer_bp = Blueprint(
        "answer",
        __name__,
        url_prefix="/answer/<int:question_id>"
    )

    @answer_bp.route("/", methods=["GET"])
    @cache.cached(timeout=3600)
    def answer(question_id):
        """
        Документация функции
        """
        with Session() as se:
            ref_path = urlparse(request.referrer).path
            if ref_path == '/statistic/':
                session['statistic'] = True
            elif ref_path == '/question/all/':
                session['question_all'] = True

            question_obj = Questions.get_question(se, question_id)
            answer_obj = Answers.get_answer(se, question_id)
            session['answer'] = answer_obj.answer
            session['question_id'] = question_obj.id
            session['question'] = question_obj.question
            session['sub_question'] = question_obj.sub_question
            return render_template('answer.html')

    return answer_bp
