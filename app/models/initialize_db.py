"""
Модуль отвечает за инициализацию и первичное заполнение базы данных.
"""

from sqlalchemy import inspect, exists, select

from app.models import engine, Session, Base
from app.models.answer import Answers
from app.models.question import Questions
from app.models.answer_options import AnswerOptions
from app.models.user import Users  # noqa
from app.models.user_statistic import UserStatistic  # noqa
from app.models.answered_questions import AnsweredQuestions  # noqa
from app.utils.processing_data import parse_question_file


def insert_initial_records() -> None:
    """
    Создаёт таблицы в базе данных и добавляет начальные записи, если они отсутствуют.

    """
    Base.metadata.create_all(engine)
    inspector = inspect(engine)
    table_exists = inspector.has_table('questions')

    with Session() as se:
        data_exists = se.execute(select(exists().where(Questions.id > 0))).scalar()
        if not table_exists or not data_exists:
            add_questions = list()
            add_answer = list()
            for data in parse_question_file():
                new_questions = Questions(question=data[1], sub_question=data[3])
                new_answer = Answers(answer=data[2], question=new_questions)
                add_questions.append(new_questions)
                add_answer.append(new_answer)
            add_answer_options = [
                AnswerOptions(choice="answered"),
                AnswerOptions(choice="partial"),
                AnswerOptions(choice="not_answered"),
            ]
            se.add_all(add_questions)
            se.add_all(add_answer)
            se.add_all(add_answer_options)
            se.commit()


insert_initial_records()
