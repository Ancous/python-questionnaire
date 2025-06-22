"""
Документация модуля
"""

from flask import Blueprint, render_template, session

from app.models import Session
from app.models.question import Questions


question_id_bp = Blueprint(
    'question_id',
    __name__,
    url_prefix="/question/<int:id>"
)


@question_id_bp.route('/', methods=['GET'])
def question_id(id):
    """
    Документация функции
    """
    if not id:
        session['message'] = "Вы знаете все ответы на вопросы. Вопросов для Вас больше нет."
        return render_template('question.html')

    with Session() as se:
        question_obj = Questions.get_question(se, id)

    session['question_id'] = question_obj.id
    session['question'] = question_obj.question
    session['sub_question'] = question_obj.sub_question
    return render_template('question.html')
