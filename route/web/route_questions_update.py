"""
Документация модуля
"""

from flask import Blueprint, flash, redirect, url_for

questions_update_bp = Blueprint(
    "questions_update",
    __name__,
    url_prefix="/questions_update"
)


@questions_update_bp.route("/", methods=["GET"])
def questions_update():
    """
    Документация функции
    """
    pass  # логика сброса истории вопросов пользователя !!!

    flash('Вопросы обновлены')
    return redirect(url_for('main.main'))
