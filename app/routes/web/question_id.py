"""
Модуль реализует обработку маршрута для отображения вопроса по идентификатору.
"""

from flask import Blueprint, render_template, session, flash
from flask.typing import ResponseReturnValue
from flask_caching import Cache

from app.models import Session
from app.models.question import Questions


def create_question_id_bp(cache: Cache) -> Blueprint:
    """
    Создаёт Blueprint для маршрута отображения вопроса по идентификатору.

    Parameters:
    cache (Cache): объект кеширования, поддерживающий метод memoize

    Return:
    question_id_bp (Blueprint): Blueprint для маршрута вопроса по id
    """
    question_id_bp = Blueprint("question_id", __name__, url_prefix="/question/<int:id>")

    @cache.memoize(timeout=5)
    def get_question_by_id(id: int) -> Questions:
        """
        Получает объект вопроса по идентификатору с кешированием.

        Parameters:
        id (int): идентификатор вопроса

        Return:
        result (Questions): объект вопроса
        """
        with Session() as se:
            result = Questions.get_question(se, id)
        return result

    @question_id_bp.route("/", methods=["GET"])
    def question_id(id: int) -> ResponseReturnValue:
        """
        Обрабатывает GET-запрос для отображения вопроса по id.

        Parameters:
        id (int): идентификатор вопроса

        Return:
        html (ResponseReturnValue): HTML-страница с вопросом
        """
        if not id:
            flash("Вы знаете все ответы на вопросы. Вопросов для Вас больше нет.")
            return render_template("question.html")

        question_obj = get_question_by_id(id)

        session["question_id"] = question_obj.id
        session_question = question_obj.question
        session_sub_question = question_obj.sub_question
        return render_template(
            "question.html",
            question=session_question,
            sub_question=session_sub_question,
        )

    return question_id_bp
