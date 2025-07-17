"""
Модуль содержит модель Questions для хранения вопросов викторины.
"""

from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from sqlalchemy import Integer, String, select, func
from sqlalchemy.orm.attributes import InstrumentedAttribute
from typing import Sequence, Union
from sqlalchemy.engine import Row

from app.models import BaseModel
from app.models.user_statistic import UserStatistic


class Questions(BaseModel):
    """
    Класс вопроса викторины.

    Arguments:
    id (int): уникальный идентификатор вопроса
    question (str): текст вопроса
    sub_question (str): дополнительный под-вопрос или пояснение
    answer (relationship): связь с правильным ответом (Answers)
    user_stats (relationship): связь со статистикой ответов пользователей (UserStatistic)
    """

    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question: Mapped[str] = mapped_column(String, nullable=False)
    sub_question: Mapped[str | None] = mapped_column(String, nullable=True)

    answer = relationship(
        "Answers",
        back_populates="question",
        uselist=False,
        cascade="all, delete-orphan",
    )

    user_stats = relationship(
        "UserStatistic", back_populates="question", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        """
        Представление объекта вопроса в виде строки.

        Return:
        str: строковое представление вопроса
        """
        return f"<Questions(id={self.id}, questions={self.question}, sub_question={self.sub_question})>"

    @classmethod
    def all_questions(cls, sesh: Session) -> Sequence["Questions"]:
        """
        Получить все объекты вопросов.

        Parameters:
        sesh (Session): сессия SQLAlchemy

        Return:
        all_questions_objects (Sequence[Questions]): список всех вопросов
        """
        stmt = select(cls)
        all_questions_objects = sesh.scalars(stmt).all()
        return all_questions_objects

    @classmethod
    def add_questions(cls, sesh: Session, questions_data: list[dict]) -> None:
        """
        Добавить несколько вопросов в базу данных.

        Parameters:
        sesh (Session): сессия SQLAlchemy
        questions_data (list[dict]): данные для добавления
        """
        questions_objects = [
            cls(question=item["question"], sub_question=item["sub_question"])
            for item in questions_data
        ]
        sesh.add_all(questions_objects)
        sesh.commit()

    @classmethod
    def update_questions(cls, sesh: Session, questions_data: list[dict]) -> None:
        """
        Обновить несколько вопросов в базе данных.

        Parameters:
        sesh (Session): сессия SQLAlchemy
        questions_data (list[dict]): данные для обновления
        """
        for item in questions_data:
            stmt = select(cls).where(cls.id == item["id"])
            question = sesh.scalars(stmt).one()
            if question:
                question.question = item["question"]
                question.sub_question = item["sub_question"]
                sesh.commit()
            else:
                raise ValueError(f"id {item['id']} не найден для изменения.")

    @classmethod
    def delete_questions(cls, sesh: Session, questions_id: list[dict]) -> None:
        """
        Удалить несколько вопросов по id.

        Parameters:
        sesh (Session): сессия SQLAlchemy
        questions_id (list[dict]): список id для удаления
        """
        for item in questions_id:
            stmt = select(cls).where(cls.id == item["id"])
            question_to_delete = sesh.scalars(stmt).one()
            if question_to_delete is None:
                raise ValueError(f"id {item['id']} не найден для удаления.")
            sesh.delete(question_to_delete)
        sesh.commit()

    @classmethod
    def get_question(cls, sesh: Session, question_id: int) -> "Questions":
        """
        Получить объект вопроса по id.

        Parameters:
        sesh (Session): сессия SQLAlchemy
        question_id (int): id вопроса

        Return:
        question_object (Questions): найденный объект вопроса
        """
        question_object = sesh.get(cls, question_id)
        if question_object is None:
            raise ValueError(f"id {question_id} не найден.")
        return question_object

    @classmethod
    def create_question(cls, sesh: Session, question_data: dict) -> None:
        """
        Создать новый вопрос (реализация не указана).

        Parameters:
        sesh (Session): сессия SQLAlchemy
        question_data (dict): данные для создания
        """
        pass

    @classmethod
    def update_question(
        cls, sesh: Session, question_id: int, question_data: dict
    ) -> None:
        """
        Обновить вопрос по id.

        Parameters:
        sesh (Session): сессия SQLAlchemy
        question_id (int): id вопроса
        question_data (dict): новые данные
        """
        stmt = select(cls).where(cls.id == question_id)
        question = sesh.scalars(stmt).one()
        if question:
            question.question = question_data["question"]
            question.sub_question = question_data["sub_question"]
            sesh.commit()
        else:
            raise ValueError(f"id {question_id} не найден для изменения.")

    @classmethod
    def delete_question(cls, sesh: Session, question_id: int) -> None:
        """
        Удалить вопрос по id.

        Parameters:
        sesh (Session): сессия SQLAlchemy
        question_id (int): id вопроса
        """
        stmt = select(cls).where(cls.id == question_id)
        question_to_delete = sesh.scalars(stmt).one()
        if question_to_delete is None:
            raise ValueError(f"id {question_id} не найден для удаления.")
        sesh.delete(question_to_delete)
        sesh.commit()

    @classmethod
    def get_random_unanswered_question(
        cls, sesh: Session, answered_ids: list[int] | None
    ) -> Union["Questions", None]:
        """
        Получить случайный неотвеченный вопрос для пользователя.

        Parameters:
        sesh (Session): сессия SQLAlchemy
        answered_ids (list[int] | None): список id уже отвеченных вопросов

        Return:
        question_obj (Questions | None): случайный неотвеченный вопрос или None
        """
        if answered_ids is None:
            answered_ids = list()
        stmt = select(cls).where(~cls.id.in_(answered_ids)).order_by(func.random())
        question_obj = sesh.scalars(stmt).first()
        return question_obj

    @classmethod
    def get_questions_grouped_by_answer_option(
        cls, sesh: Session, user_id: int
    ) -> Sequence[Row]:
        """
        Получить вопросы, сгруппированные по выбранному варианту ответа пользователя.

        Parameters:
        sesh (Session): сессия SQLAlchemy
        user_id (int): id пользователя

        Return:
        result (Sequence[Row]): список строк с answer_option_id, id вопроса, текст вопроса
        """
        userstatistic_userid: InstrumentedAttribute = UserStatistic.user_id
        stmt = (
            select(UserStatistic.answer_option_id, Questions.id, Questions.question)
            .join(Questions, UserStatistic.question)
            .where(userstatistic_userid == user_id)
            .order_by(UserStatistic.answer_option_id)
        )
        result = sesh.execute(stmt).all()
        return result

    @classmethod
    def get_by_name_question(cls, sesh: Session, name_questions: str) -> "Questions":
        """
        Получить вопрос по его тексту.

        Parameters:
        sesh (Session): сессия SQLAlchemy
        name_questions (str): текст вопроса

        Return:
        question_obj (Questions): найденный объект вопроса
        """
        stmt = select(cls).where(cls.question == name_questions)
        question_obj = sesh.scalars(stmt).one()
        return question_obj
