"""
Документация модуля
"""

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, select

from app.models import BaseModel


class Questions(BaseModel):
    """
    Документация класса
    """
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(String)
    sub_question = Column(String)

    answer = relationship("Answers", back_populates="question", cascade="all, delete-orphan")

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
        query = (
            select(Questions)
        )
        result = sesh.execute(query)
        all_questions_objects = result.scalars().all()
        return all_questions_objects

    @classmethod
    def add_questions(cls, sesh, questions_data):
        """
        Документация метода
        """
        questions_objects = [
            Questions(
                question=item["question"],
                sub_question=item["sub_question"]
            ) for item in questions_data
        ]
        sesh.add_all(questions_objects)
        sesh.commit()

    @classmethod
    def update_questions(cls, sesh, questions_data):
        """
        Документация метода
        """
        for item in questions_data:
            question = sesh.query(Questions).filter(Questions.id == item["id"]).first()
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
            question_to_delete = sesh.query(Questions).filter(Questions.id == item["id"]).one_or_none()
            if question_to_delete is None:
                raise ValueError(f"id {item["id"]} не найден для удаления.")
            sesh.delete(question_to_delete)

        sesh.commit()

    @classmethod
    def get_question(cls, sesh, question_id):
        """
        Документация метода
        """
        question_object = sesh.get(Questions, question_id)
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
        question = sesh.query(Questions).filter(Questions.id == question_id).first()
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
        question_to_delete = sesh.query(Questions).filter(Questions.id == question_id).one_or_none()
        if question_to_delete is None:
            raise ValueError(f"id {question_id} не найден для удаления.")
        sesh.delete(question_to_delete)

        sesh.commit()
