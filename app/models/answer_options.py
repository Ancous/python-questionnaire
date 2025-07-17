"""
Модуль содержит модель AnswerOptions для хранения вариантов ответов пользователя на вопросы.
"""

from sqlalchemy import Integer, String, select
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session

from app.models import BaseModel


class AnswerOptions(BaseModel):
    """
    Класс варианта ответа пользователя на вопрос.

    Arguments:
    id (int): уникальный идентификатор варианта ответа
    choice (str): текстовое значение варианта (например, 'answered')
    user_stats (relationship): связь с UserStatistic, отражающая пользователей, выбравших этот вариант
    """

    __tablename__ = "answer_options"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    choice: Mapped[str] = mapped_column(String, nullable=False)

    user_stats = relationship(
        "UserStatistic", back_populates="answer_option", cascade="all, delete-orphan"
    )

    @classmethod
    def get_by_choice(cls, sesh: Session, choice: str) -> "AnswerOptions":
        """
        Получить вариант ответа по его значению.

        Parameters:
        sesh (Session): сессия SQLAlchemy
        choice (str): текстовое значение варианта

        Return:
        result (AnswerOptions): найденный вариант ответа
        """
        stmt = select(cls).where(cls.choice == choice)
        result = sesh.scalars(stmt).one()
        return result
