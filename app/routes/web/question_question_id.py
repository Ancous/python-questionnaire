"""
Документация модуля
"""

from flask import Blueprint, render_template, session

from app.models import Session
from app.models.question import Questions


def create_question_question_id_bp(cache):
    """
    Документация функции
    """
    question_question_id_bp = Blueprint(
        'question_question_id',
        __name__,
        url_prefix="/question/<int:question_id>"
    )

    @question_question_id_bp.route('/', methods=['GET'])
    @cache.cached(timeout=3600)
    def question_question_id(question_id):
        """
        Документация функции
        """
        if not question_id:
            session['message'] = "Вы знаете все ответы на вопросы. Вопросов для Вас больше нет."
            return render_template('question.html')

        with Session() as se:
            question_obj = Questions.get_question(se, question_id)

        session['question_id'] = question_obj.id
        session['question'] = question_obj.question
        session['sub_question'] = question_obj.sub_question
        return render_template('question.html')

    return question_question_id_bp
