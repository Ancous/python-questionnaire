"""
Модуль содержит модель UserStatistic для хранения статистики ответов пользователей на вопросы.
"""

from sqlalchemy import Integer, ForeignKey, select, UniqueConstraint, delete
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from typing import Sequence, Union

from app.models import BaseModel


class UserStatistic(BaseModel):
    """
    Класс для хранения статистики ответов пользователя на вопросы.

    Arguments:
    id (int): уникальный идентификатор записи
    user_id (int): внешний ключ на пользователя (Users)
    question_id (int): внешний ключ на вопрос (Questions)
    answer_option_id (int): внешний ключ на вариант ответа (AnswerOptions)
    question (relationship): связь с вопросом
    user (relationship): связь с пользователем
    answer_option (relationship): связь с вариантом ответа
    """

    __tablename__ = "user_statistic"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    question_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("questions.id"), nullable=False
    )
    answer_option_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("answer_options.id"), nullable=False
    )

    question = relationship("Questions", back_populates="user_stats")
    user = relationship("Users", back_populates="user_stats")
    answer_option = relationship("AnswerOptions", back_populates="user_stats")

    __table_args__ = (
        UniqueConstraint("user_id", "question_id", name="uq_user_question"),
    )

    def __repr__(self) -> str:
        """
        Представление объекта статистики в виде строки.

        Return:
        str: строковое представление объекта
        """
        return (
            f"<UserStatistic("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"question_id={self.question_id}, "
            f"answer_option_id={self.answer_option_id})>"
        )

    @classmethod
    def all_statistic_for_user(
        cls, sesh: Session, user_id: int
    ) -> Sequence["UserStatistic"]:
        """
        Получить всю статистику для пользователя.

        Parameters:
        sesh (Session): сессия SQLAlchemy
        user_id (int): id пользователя

        Return:
        statistic_obj (Sequence[UserStatistic]): список статистики
        """
        stmt = select(cls).where(cls.user_id == user_id)
        statistic_obj = sesh.scalars(stmt).all()
        return statistic_obj

    @classmethod
    def get_statistic_for_user_and_question(
        cls, sesh: Session, user_id: int, question_id: int
    ) -> Union["UserStatistic", None]:
        """
        Получить статистику для пользователя по конкретному вопросу.

        Parameters:
        sesh (Session): сессия SQLAlchemy
        user_id (int): id пользователя
        question_id (int): id вопроса

        Return:
        statistic_obj (UserStatistic | None): объект статистики или None
        """
        stmt = select(cls).where(cls.user_id == user_id, cls.question_id == question_id)
        statistic_obj = sesh.scalars(stmt).first()
        return statistic_obj

    @classmethod
    def set_answer_for_user_and_question(
        cls, sesh: Session, user_id: int, question_id: int, answer_option_id: int
    ) -> "UserStatistic":
        """
        Установить вариант ответа для пользователя по вопросу.

        Parameters:
        sesh (Session): сессия SQLAlchemy
        user_id (int): id пользователя
        question_id (int): id вопроса
        answer_option_id (int): id варианта ответа

        Return:
        instance (UserStatistic): объект статистики
        """
        instance = cls.get_statistic_for_user_and_question(sesh, user_id, question_id)
        if instance:
            instance.answer_option_id = answer_option_id
        else:
            instance = UserStatistic(
                user_id=user_id,
                question_id=question_id,
                answer_option_id=answer_option_id,
            )
            sesh.add(instance)
        sesh.commit()
        return instance

    @classmethod
    def delete_answer_for_user_id(cls, sesh: Session, user_id: int) -> None:
        """
        Удалить все ответы пользователя из статистики.

        Parameters:
        sesh (Session): сессия SQLAlchemy
        user_id (int): id пользователя
        """
        sesh.execute(delete(cls).where(cls.user_id == user_id))
        sesh.commit()
