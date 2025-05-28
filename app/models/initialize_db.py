"""
Документация модуля
"""

from sqlalchemy import inspect, exists

from app.models import engine, Session, Base
from app.models.answer import Answers
from app.models.question import Questions
from app.utils.data_processing import parse_question_file


def insert_initial_records():
    """
    Документация функции
    """
    Base.metadata.create_all(engine)

    with Session() as se:
        inspector = inspect(engine)
        table_exists = inspector.has_table('questions')
        data_exists = se.query(exists().where(Questions.id > 0)).scalar()
        if not table_exists or not data_exists:
            add_questions = list()
            add_answer = list()
            for data in parse_question_file():
                new_questions = Questions(question=data[1], sub_question=data[3])
                new_answer = Answers(answer=data[2], question=new_questions)
                add_questions.append(new_questions)
                add_answer.append(new_answer)
            se.add_all(add_questions)
            se.add_all(add_answer)
            se.commit()


insert_initial_records()
