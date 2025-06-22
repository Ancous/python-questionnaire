"""
Документация модуля
"""

from urllib.parse import urlparse

from flask import Blueprint, render_template, session, request

from app.models import Session
from app.models.answer import Answers
from app.models.question import Questions


answer_id_bp = Blueprint(
    "answer_id",
    __name__,
    url_prefix="/answer/<int:id>"
)


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

    with Session() as se:
        answer_obj = Answers.answer_by_question_id(se, id)
        question_obj = Questions.get_question(se, id)
        session['answer_id'] = answer_obj.id
        session['answer'] = answer_obj.answer
        session['question_id'] = question_obj.id
        session['question'] = question_obj.question
        session['sub_question'] = question_obj.sub_question
        return render_template('answer.html')
