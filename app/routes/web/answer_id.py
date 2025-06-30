"""
Документация модуля
"""

from urllib.parse import urlparse

from flask import Blueprint, render_template, session, request

from app.models import Session
from app.models.answer import Answers
from app.models.question import Questions


def create_answer_id_bp(cache):
    """
    Документация функции
    """
    answer_id_bp = Blueprint(
        "answer_id",
        __name__,
        url_prefix="/answer/<int:id>"
    )

    @cache.memoize(timeout=5)
    def get_question_answer_by_id(id):
        """
        Документация функции
        """
        with Session() as se:
            result_1 = Answers.answer_by_question_id(se, id)
            result_2 = Questions.get_question(se, id)

        return result_1, result_2

    @answer_id_bp.route("/", methods=["GET"])
    def answer_id(id):
        """
        Документация функции
        """
        ref_path = urlparse(request.referrer).path
        if ref_path == '/statistic/':
            session['statistic'] = True
        elif ref_path == '/question/all/':
            session['question_all'] = True

        answer_obj, question_obj = get_question_answer_by_id(id)
        session["question_id"] = question_obj.id
        session_answer_id = answer_obj.id
        session_answer = answer_obj.answer
        session_question = question_obj.question
        session_sub_question = question_obj.sub_question
        return render_template(
            'answer.html',
            answer_id=session_answer_id,
            answer=session_answer,
            question=session_question,
            sub_question=session_sub_question
        )

    return answer_id_bp
