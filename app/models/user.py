"""
Документация модуля
"""

from sqlalchemy import String, Integer, select
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import BaseModel


class Users(BaseModel):
    """
    Документация класса
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

    def __repr__(self):
        """
        Документация метода
        """
        return f"<Answer(id={self.id}, answer={self.username})>"

    @classmethod
    def get_user(cls, sesh, username) -> list:
        """
        Документация метода
        """
        stmt = select(cls).where(cls.username == username)
        user_obj = sesh.execute(stmt).scalars().first()
        return user_obj

    @classmethod
    def add_user(cls, sesh, username, hashed_pw):
        """
        Документация метода
        """
        user = cls(username=username, password=hashed_pw)
        sesh.add(user)
        sesh.commit()
        return user
