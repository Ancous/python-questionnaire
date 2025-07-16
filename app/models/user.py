"""
Модуль содержит модель Users для хранения информации о пользователях системы.
"""

from sqlalchemy import String, Integer, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from typing import Union

from app.models import BaseModel


class Users(BaseModel):
    """
    Класс пользователя системы.

    Arguments:
    id (int): уникальный идентификатор пользователя
    username (str): имя пользователя (логин)
    password (str): хэш пароля пользователя
    answered_questions (relationship): связь с отвеченными вопросами (AnsweredQuestions)
    user_stats (relationship): связь со статистикой ответов (UserStatistic)
    """
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)

    answered_questions = relationship(
        "AnsweredQuestions",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    user_stats = relationship(
        "UserStatistic",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        """
        Представление объекта пользователя в виде строки.

        Return:
        str: строковое представление пользователя
        """
        return f"<Answer(id={self.id}, answer={self.username})>"

    @classmethod
    def get_user(cls, sesh: Session, username: str) -> Union["Users", None]:
        """
        Получить пользователя по имени.

        Parameters:
        sesh (Session): сессия SQLAlchemy
        username (str): имя пользователя

        Return:
        user_obj (Users | None): найденный пользователь или None
        """
        stmt = select(cls).where(cls.username == username)
        user_obj = sesh.execute(stmt).scalars().first()
        return user_obj

    @classmethod
    def add_user(cls, sesh: Session, username: str, hashed_pw: str) -> "Users":
        """
        Добавить нового пользователя.

        Parameters:
        sesh (Session): сессия SQLAlchemy
        username (str): имя пользователя
        hashed_pw (str): хэш пароля

        Return:
        user (Users): созданный пользователь
        """
        user = cls(username=username, password=hashed_pw)
        sesh.add(user)
        sesh.commit()
        return user
