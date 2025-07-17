"""
Модуль содержит модель AnsweredQuestions для отслеживания номеров вопросов, на которые пользователь уже ответил.
"""

from sqlalchemy import Integer, JSON, ForeignKey, select, func
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session

from app.models import BaseModel


class AnsweredQuestions(BaseModel):
    """
    Класс для хранения списка номеров вопросов, на которые пользователь уже ответил.

    Arguments:
    id (int): уникальный идентификатор записи
    numbers (list[int]): список номеров отвеченных вопросов (JSON)
    user_id (int): внешний ключ на пользователя (Users)
    user (relationship): связь с пользователем
    """

    __tablename__ = "answered_questions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    numbers: Mapped[list] = mapped_column(MutableList.as_mutable(JSON), nullable=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), unique=True, nullable=False
    )

    user = relationship("Users", back_populates="answered_questions", uselist=False)

    def __repr__(self) -> str:
        """
        Представление объекта отвеченных вопросов в виде строки.

        Return:
        str: строковое представление объекта
        """
        return f"<AnsweredQuestions(id={self.id}, numbers={self.numbers})>"

    @classmethod
    def get_numbers(cls, sesh: Session, user_id: int) -> list[int] | None:
        """
        Получить список номеров отвеченных вопросов для пользователя.

        Parameters:
        sesh (Session): сессия SQLAlchemy
        user_id (int): id пользователя

        Return:
        answered_questions_numbers (list[int] | None): список номеров или None
        """
        stmt = select(cls.numbers).where(cls.user_id == user_id)
        answered_questions_numbers = sesh.scalars(stmt).one_or_none()
        return answered_questions_numbers

    @classmethod
    def get_numbers_count(cls, sesh: Session, user_id: int) -> int:
        """
        Получить количество отвеченных вопросов для пользователя.

        Parameters:
        sesh (Session): сессия SQLAlchemy
        user_id (int): id пользователя

        Return:
        count (int): количество отвеченных вопросов
        """
        stmt = select(func.json_array_length(cls.numbers)).where(cls.user_id == user_id)
        count = sesh.scalars(stmt).one_or_none()
        return count or 0

    @classmethod
    def mark_question_as_answered(
        cls, sesh: Session, user_id: int, number_question: int
    ) -> None:
        """
        Отметить вопрос как отвеченный для пользователя.

        Parameters:
        sesh (Session): сессия SQLAlchemy
        user_id (int): id пользователя
        number_question (int): номер вопроса
        """
        stmt = select(cls).where(cls.user_id == user_id)
        answered_questions_numbers = sesh.scalars(stmt).one_or_none()
        if answered_questions_numbers is None:
            answered_question = cls(numbers=[number_question], user_id=user_id)
            sesh.add(answered_question)
        else:
            if number_question not in answered_questions_numbers.numbers:
                answered_questions_numbers.numbers.append(number_question)
        sesh.commit()

    @classmethod
    def remove_question_from_marked(
        cls, sesh: Session, user_id: int, number_question: int
    ) -> None:
        """
        Удалить вопрос из списка отвеченных для пользователя.

        Parameters:
        sesh (Session): сессия SQLAlchemy
        user_id (int): id пользователя
        number_question (int): номер вопроса
        """
        stmt = select(cls).where(cls.user_id == user_id)
        answered_questions_numbers = sesh.scalars(stmt).one_or_none()
        if (
            answered_questions_numbers
            and number_question in answered_questions_numbers.numbers
        ):
            answered_questions_numbers.numbers.remove(number_question)
        sesh.commit()

    @classmethod
    def clear_answered_questions(cls, sesh: Session, user_id: int) -> None:
        """
        Очистить список отвеченных вопросов для пользователя.

        Parameters:
        sesh (Session): сессия SQLAlchemy
        user_id (int): id пользователя
        """
        stmt = select(cls).where(cls.user_id == user_id)
        answered_questions_numbers = sesh.scalars(stmt).one_or_none()
        if answered_questions_numbers:
            answered_questions_numbers.numbers.clear()
            sesh.commit()
