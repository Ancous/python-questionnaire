"""
Модуль для обработки истории ответов пользователя.

Содержит функцию для обновления статистики ответов пользователя и взаимодействия с моделями AnswerOptions, AnsweredQuestions и UserStatistic.
"""
from flask import session

from app.config.config import NUMBER_OF_QUESTIONS
from app.models.answer_options import AnswerOptions
from app.models.answered_questions import AnsweredQuestions
from app.models.user_statistic import UserStatistic
from sqlalchemy.orm import Session


def process_user_answer(
    se: Session,
    user_id: int,
    question_id: int,
    action: str,
    statistic_questionall: bool
) -> None:
    """
    Обновляет статистику ответов пользователя и взаимодействует с моделями AnswerOptions, AnsweredQuestions и UserStatistic.

    Parameters:
    se (Session): сессия SQLAlchemy
    user_id (int): идентификатор пользователя
    question_id (int): идентификатор вопроса
    action (str): действие пользователя ('answered', 'partial', 'not_answered')
    statistic_questionall (bool): учитывать ли вопрос в общей статистике
    """
    answer_choices: dict[str, str] = {
        'answered': 'answered',
        'partial': 'partial',
        'not_answered': 'not_answered'
    }
    choice: str | None = answer_choices.get(action)
    if choice is None:
        raise ValueError(f"Недопустимое значение action: {action}")
    answer_option = AnswerOptions.get_by_choice(se, choice)

    if action == 'answered':
        AnsweredQuestions.mark_question_as_answered(se, user_id, question_id)
    if statistic_questionall:
        if action in ('partial', 'not_answered'):
            AnsweredQuestions.remove_question_from_marked(se, user_id, question_id)

    session['number_questions_answered'] = NUMBER_OF_QUESTIONS - AnsweredQuestions.get_numbers_count(se, user_id=session["user_id"])
    UserStatistic.set_answer_for_user_and_question(se, user_id, question_id, answer_option.id)
