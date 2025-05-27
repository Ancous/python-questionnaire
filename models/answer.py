"""
Документация модуля
"""

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey

from models import BaseModel


class Answers(BaseModel):
    """
    Документация класса
    """
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True, autoincrement=True)

    answer = Column(String)
    question_id = Column(Integer, ForeignKey('questions.id'))

    question = relationship("Questions", back_populates="answer")

    def __repr__(self):
        """
        Документация метода
        """
        return f"<Answer(id={self.id}, answer={self.answer}, question_id={self.question_id})>"
