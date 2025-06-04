"""
Документация модуля
"""

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, select, func

from app.models import BaseModel


class Questions(BaseModel):
    """
    Документация класса
    """
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(String, nullable=False)
    sub_question = Column(String)

    answer = relationship(
        "Answers",
        back_populates="question",
        uselist=False,
        cascade="all, delete-orphan"
    )

    user_stats = relationship(
        "UserStatistic",
        back_populates="question"
    )

    def __repr__(self):
        """
        Документация метода
        """
        return f"<Questions(id={self.id}, questions={self.question}, sub_question={self.sub_question})>"

    @classmethod
    def all_questions(cls, sesh) -> list:
        """
        Документация метода
        """
        all_questions_objects = sesh.execute(select(cls)).scalars().all()
        return all_questions_objects

    @classmethod
    def add_questions(cls, sesh, questions_data):
        """
        Документация метода
        """
        questions_objects = [
            cls(question=item["question"], sub_question=item["sub_question"])
            for item in questions_data
        ]
        sesh.add_all(questions_objects)
        sesh.commit()

    @classmethod
    def update_questions(cls, sesh, questions_data):
        """
        Документация метода
        """
        for item in questions_data:
            stmt = select(cls).where(cls.id == item["id"])
            question = sesh.execute(stmt).scalars().first()
            if question:
                question.question = item["question"]
                question.sub_question = item["sub_question"]
                sesh.commit()
            else:
                raise ValueError(f"id {item["id"]} не найден для изменения.")

    @classmethod
    def delete_questions(cls, sesh, questions_id):
        """
        Документация метода
        """
        for item in questions_id:
            stmt = select(cls).where(cls.id == item["id"])
            question_to_delete = sesh.execute(stmt).scalars().first()
            if question_to_delete is None:
                raise ValueError(f"id {item["id"]} не найден для удаления.")
            sesh.delete(question_to_delete)

        sesh.commit()

    @classmethod
    def get_question(cls, sesh, question_id):
        """
        Документация метода
        """
        question_object = sesh.get(cls, question_id)
        if question_object is None:
            raise ValueError(f"id {question_id} не найден.")

        return question_object

    @classmethod
    def create_question(cls, sesh, question_data):
        """
        Документация метода
        """
        pass

    @classmethod
    def update_question(cls, sesh, question_id, question_data):
        """
        Документация метода
        """
        stmt = select(cls).where(cls.id == question_id)
        question = sesh.execute(stmt).scalars().first()
        if question:
            question.question = question_data["question"]
            question.sub_question = question_data["sub_question"]
            sesh.commit()
        else:
            raise ValueError(f"id {question_id} не найден для изменения.")

    @classmethod
    def delete_question(cls, sesh, question_id):
        """
        Документация метода
        """
        stmt = select(cls).where(cls.id == question_id)
        question_to_delete = sesh.execute(stmt).scalars().first()
        if question_to_delete is None:
            raise ValueError(f"id {question_id} не найден для удаления.")
        sesh.delete(question_to_delete)

        sesh.commit()

    @classmethod
    def get_random_unanswered_question(cls, sesh, answered_ids):
        """
        Документация метода
        """
        if answered_ids is None:
            answered_ids = list()
        stmt = (
            select(cls)
            .where(~cls.id.in_(answered_ids))
            .order_by(func.random())
        )
        question_obj = sesh.execute(stmt).scalars().first()
        return question_obj
