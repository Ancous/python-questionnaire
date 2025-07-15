"""
Документация модуля
"""

from sqlalchemy import Integer, String, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import BaseModel


class AnswerOptions(BaseModel):
    """
    Документация класса
    """
    __tablename__ = 'answer_options'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    choice: Mapped[str] = mapped_column(String, nullable=False)

    user_stats = relationship(
        "UserStatistic",
        back_populates="answer_option",
        cascade="all, delete-orphan"
    )

    @classmethod
    def get_by_choice(cls, sesh, choice):
        """
        Документация метода
        """
        stmt = select(cls).where(cls.choice == choice)
        result = sesh.scalars(stmt).one()
        return result
