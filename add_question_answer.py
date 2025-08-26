"""
Модуль для добавления вопросов и ответов в базу данных PostgreSQL.
Содержит классы моделей SQLAlchemy для вопросов и ответов, а также функции для парсинга и добавления данных в базу.
"""

import re

from sqlalchemy import create_engine, select, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, DeclarativeBase, relationship

from app.utils.processing_data import parse_question_file

POSTGRES_URL: str = "postgresql://root:1975@31.129.100.106:5432/python_interview"
QUESTION_PATTERN: re.Pattern = re.compile(
    r"### (?P<number_question>\d+).\s+(?P<question>.*?)"
    r"\s+(?P<trash>&nbsp;\s*)*<small>\[Ответ](?P<link>.*)</small>",
)
ANSWER_LINK_PREFIX: str = "[Ответ]("
ANSWER_LINK_SUFFIX: str = ")"
IGNORE_LINE_PREFIXES: tuple[str, ...] = (
    "<div",
    "[Вернуться к вопросам]",
    "</div",
    "\n",
)
CODEBLOCK: str = "```"


class Base(DeclarativeBase):
    """
    Базовый класс для моделей SQLAlchemy.
    """


class Answers(Base):
    """
    Класс модели ответа для таблицы 'answers'.

    Arguments:
    id (int): идентификатор ответа
    answer (str): текст ответа
    question_id (int): внешний ключ на вопрос
    question (Questions): связь с вопросом
    """

    __tablename__ = "answers"
    id = Column(Integer, primary_key=True, autoincrement=True)

    answer = Column(String, nullable=False)
    question_id = Column(
        Integer, ForeignKey("questions.id"), unique=True, nullable=False
    )
    question = relationship("Questions", back_populates="answer", uselist=False)


class Questions(Base):
    """
    Класс модели вопроса для таблицы 'questions'.

    Arguments:
    id (int): идентификатор вопроса
    question (str): текст вопроса
    sub_question (str): дополнительный вопрос
    answer (Answers): связь с ответом
    """

    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(String, nullable=False)
    sub_question = Column(String)
    answer = relationship(
        "Answers",
        back_populates="question",
        uselist=False,
        cascade="all, delete-orphan",
    )


def parse_answer_db(se: sessionmaker) -> list[str]:
    """
    Функция для получения всех ответов из базы данных.

    Parameters:
    se (sessionmaker): фабрика сессий SQLAlchemy

    Return:
    list[str]: список всех ответов из базы
    """
    finish_result = list()

    with se() as sess:
        stmt = select(Answers)
        itog = sess.execute(stmt)
        record = itog.scalars().all()
    for obj_answer in record:
        finish_result.append(obj_answer.answer)

    return finish_result


def func_add_question_answer(
    se: sessionmaker, all_que: list[list], all_ans_db: list[str]
) -> None:
    """
    Функция для добавления новых вопросов и ответов в базу данных.

    Parameters:
    se (sessionmaker): фабрика сессий SQLAlchemy
    all_que (list[list]): список вопросов и связанных данных
    all_ans_db (list[str]): список уже существующих ответов в базе
    """
    add_questions = list()
    add_answer = list()

    with se() as session:
        for question_data in all_que:
            if question_data[2] not in all_ans_db:
                new_questions = Questions(
                    question=question_data[1], sub_question=question_data[3]
                )
                new_answer = Answers(answer=question_data[2], question=new_questions)
                add_questions.append(new_questions)
                add_answer.append(new_answer)
        session.add_all(add_questions)
        session.add_all(add_answer)
        session.commit()


if __name__ == "__main__":
    engine = create_engine(POSTGRES_URL)
    Session = sessionmaker(engine)

    all_question = parse_question_file()
    all_answer_db = parse_answer_db(Session)
    func_add_question_answer(Session, all_question, all_answer_db)
