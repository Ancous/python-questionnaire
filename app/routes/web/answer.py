"""
Документация модуля
"""
from urllib.parse import urlparse

from flask import Blueprint, render_template, session, request

from app.models import Session
from app.models.answer import Answers
from app.models.question import Questions

answer_bp = Blueprint(
    "answer",
    __name__,
    url_prefix="/answer"
)


@answer_bp.route("/<string:name>", methods=["GET"])
@answer_bp.route("/", defaults={'name': None}, methods=["GET"])
def answer(name):
    """
    Документация функции
    """
    with Session() as se:
        if name is None:
            answer_obj = Answers.answer_by_question_id(se, session["question_id"])
            session['answer'] = answer_obj.answer
            return render_template('answer.html')
        else:
            ref_path = urlparse(request.referrer).path
            if ref_path == '/statistic/':
                session['statistic'] = True
            elif ref_path == '/question/all/':
                session['question_all'] = True

            question_obj = Questions.get_by_name_question(se, name)
            answer_obj = Answers.answer_by_question_id(se, question_obj.id)
            session['answer'] = answer_obj.answer
            session['question_id'] = question_obj.id
            session['question'] = question_obj.question
            session['sub_question'] = question_obj.sub_question
            return render_template('answer.html')
