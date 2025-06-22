"""
Документация модуля
"""
from flask import session

from app.models.answer_options import AnswerOptions
from app.models.answered_questions import AnsweredQuestions
from app.models.user_statistic import UserStatistic


def process_user_answer(se, user_id: int, question_id: int, action: str, statistic_questionall: bool) -> None:
    """
    Документация функции
    """
    answer_choices = {
        'answered': 'answered',
        'partial': 'partial',
        'not_answered': 'not_answered'
    }
    choice = answer_choices.get(action)
    answer_option = AnswerOptions.get_by_choice(se, choice)

    if action == 'answered':
        AnsweredQuestions.mark_question_as_answered(se, user_id, question_id)
    if statistic_questionall:
        if action in ('partial', 'not_answered'):
            AnsweredQuestions.remove_question_from_marked(se, user_id, question_id)

    session['number_questions_answered'] = 200 - AnsweredQuestions.get_numbers_count(se, user_id=session["user_id"])
    UserStatistic.set_answer_for_user_and_question(se, user_id, question_id, answer_option.id)
