"""
Документация модуля
"""

from flask import Blueprint, render_template, session

from app.models import Session
from app.models.question import Questions


def create_question_id_bp(cache):
    """
    Документация функции
    """
    question_id_bp = Blueprint(
        'question_id',
        __name__,
        url_prefix="/question/<int:id>"
    )

    @cache.memoize(timeout=5)
    def get_question_by_id(id):
        """
        Документация функции
        """
        with Session() as se:
            result = Questions.get_question(se, id)

        return result

    @question_id_bp.route('/', methods=['GET'])
    def question_id(id):
        """
        Документация функции
        """
        if not id:
            session['message'] = "Вы знаете все ответы на вопросы. Вопросов для Вас больше нет."
            return render_template('question.html')

        question_obj = get_question_by_id(id)

        session['question_id'] = question_obj.id
        session['question'] = question_obj.question
        session['sub_question'] = question_obj.sub_question
        return render_template('question.html')

    return question_id_bp
