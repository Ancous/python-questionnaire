"""
Модуль реализует обработку маршрута для отображения всех вопросов.
"""
import time

from flask import Blueprint, render_template, session
from flask.typing import ResponseReturnValue
from flask_caching import Cache

from app.models import Session
from app.models.question import Questions


def create_question_all_bp(cache: Cache) -> Blueprint:
    """
    Создаёт Blueprint для маршрута отображения всех вопросов.

    Parameters:
    cache (Cache): объект кеширования, поддерживающий метод cached

    Return:
    question_all_bp (Blueprint): Blueprint для маршрута всех вопросов
    """
    question_all_bp = Blueprint(
        'question_all',
        __name__,
        url_prefix="/question/all"
    )

    @question_all_bp.route('/', methods=["GET"])
    @cache.cached(timeout=5)
    def question_all() -> ResponseReturnValue:
        """
        Обрабатывает GET-запрос для отображения всех вопросов.

        Return:
        html (ResponseReturnValue): HTML-страница со списком всех вопросов
        """
        session['statistic'] = None
        session['question_all'] = None
        with Session() as se:
            question_obj = Questions.all_questions(se)
            result = [{"id": q.id, "question": q.question, "sub_question": q.sub_question} for q in question_obj]
        return render_template('question_all.html', question_all=result)

    return question_all_bp
