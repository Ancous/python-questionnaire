"""
Документация модуля
"""

from sqlalchemy import Column, Integer, JSON, ForeignKey, select, func
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import relationship

from app.models import BaseModel


class AnsweredQuestions(BaseModel):
    """
    Документация класса
    """
    __tablename__ = 'answered_questions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    numbers = Column(MutableList.as_mutable(JSON), nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True, nullable=False)

    user = relationship(
        "Users",
        back_populates="answered_questions",
        uselist=False
    )

    def __repr__(self):
        return f"<AnsweredQuestions(id={self.id}, numbers={self.numbers})>"

    @classmethod
    def get_numbers(cls, sesh, user_id) -> list:
        """
        Документация метода
        """
        stmt = select(cls.numbers).where(cls.user_id == user_id)
        answered_questions_numbers = sesh.execute(stmt).scalars().first()
        return answered_questions_numbers

    @classmethod
    def get_numbers_count(cls, sesh, user_id) -> int:
        """
        Документация метода
        """
        stmt = select(func.json_array_length(cls.numbers)).where(cls.user_id == user_id)
        count = sesh.execute(stmt).scalar()
        return count or 0

    @classmethod
    def mark_question_as_answered(cls, sesh, user_id, number_question):
        """
        Документация метода
        """
        stmt = select(cls).where(cls.user_id == user_id)
        answered_questions_numbers = sesh.execute(stmt).scalars().first()
        if answered_questions_numbers is None:
            answered_question = cls(numbers=[number_question], user_id=user_id)
            sesh.add(answered_question)
            sesh.commit()
        else:
            answered_questions_numbers.numbers.append(number_question)
            sesh.commit()

    @classmethod
    def clear_answered_questions(cls, sesh, user_id):
        """
        Документация метода
        """
        stmt = select(cls).where(cls.user_id == user_id)
        answered_questions_numbers = sesh.execute(stmt).scalars().first()
        if answered_questions_numbers:
            answered_questions_numbers.numbers.clear()
            sesh.commit()
