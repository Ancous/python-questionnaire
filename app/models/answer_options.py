"""
Документация модуля
"""

from sqlalchemy import Column, Integer, String, select
from sqlalchemy.orm import relationship

from app.models import BaseModel


class AnswerOptions(BaseModel):
    """
    Документация класса
    """
    __tablename__ = 'answer_options'

    id = Column(Integer, primary_key=True, autoincrement=True)
    choice = Column(String, nullable=False)

    user_stats = relationship(
        "UserStatistic",
        back_populates="answer_option"
    )

    @classmethod
    def get_by_choice(cls, sesh, choice):
        """
        Документация метода
        """
        stmt = select(cls).where(cls.choice == choice)
        result = sesh.execute(stmt).scalars().first()
        return result
