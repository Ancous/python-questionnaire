"""
Документация модуля
"""

from flask import Blueprint, flash, redirect, url_for

question_update_bp = Blueprint(
    "question_update",
    __name__,
    url_prefix="/question_update"
)


@question_update_bp.route("/", methods=["GET"])
def question_update():
    """
    Документация функции
    """
    pass  # логика сброса истории вопросов пользователя !!!

    flash('Вопросы обновлены')
    return redirect(url_for('main.main'))
