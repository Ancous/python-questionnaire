"""
Документация модуля
"""

from sqlalchemy import Column, Integer, ForeignKey, select, UniqueConstraint
from sqlalchemy.orm import relationship

from app.models import BaseModel


class UserStatistic(BaseModel):
    """
    Документация класса
    """
    __tablename__ = 'user_statistic'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    question_id = Column(Integer, ForeignKey('questions.id'), nullable=False)
    answer_option_id = Column(Integer, ForeignKey('answer_options.id'), nullable=False)

    question = relationship(
        "Questions",
        back_populates="user_stats"
    )
    user = relationship(
        "Users",
        back_populates="user_stats"
    )
    answer_option = relationship(
        "AnswerOptions",
        back_populates="user_stats"
    )

    __table_args__ = (
        UniqueConstraint('user_id', 'question_id', name='uq_user_question'),
    )

    def __repr__(self):
        """
        Документация метода
        """
        return (
            f"<UserStatistic("
            f"id={self.id}, "
            f"user_id={self.user_id}, "
            f"question_id={self.question_id}, "
            f"answer_option_id={self.answer_option_id})>"
        )

    @classmethod
    def all_statistic_for_user(cls, sesh, user_id) -> list:
        """
        Документация метода
        """
        stmt = select(cls).where(cls.user_id == user_id)
        statistic_obj = sesh.scalars(stmt).all()
        return statistic_obj

    @classmethod
    def get_statistic_for_user_and_question(cls, sesh, user_id, question_id) -> list:
        """
        Документация метода
        """
        stmt = select(cls).where(cls.user_id == user_id, cls.question_id == question_id)
        statistic_obj = sesh.scalars(stmt).first()
        return statistic_obj

    @classmethod
    def set_answer_for_user_and_question(cls, sesh, user_id, question_id, answer_option_id):
        """
        Документация метода
        """
        instance = cls.get_statistic_for_user_and_question(sesh, user_id, question_id)

        if instance:
            instance.answer_option_id = answer_option_id
        else:
            instance = UserStatistic(
                user_id=user_id,
                question_id=question_id,
                answer_option_id=answer_option_id
            )
            sesh.add(instance)
        sesh.commit()
        return instance
