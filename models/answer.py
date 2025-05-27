"""
Документация модуля
"""

from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, select

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

    @classmethod
    def all_answers(cls, sesh) -> list:
        """
        Документация метода
        """
        query = (
            select(Answers)
        )
        result = sesh.execute(query)
        all_answers_objects = result.scalars().all()
        return all_answers_objects

    @classmethod
    def add_answers(cls, sesh, answers_data):
        """
        Документация метода
        """
        answers_objects = [
            Answers(
                answer=item["answer"]
            ) for item in answers_data
        ]
        sesh.add_all(answers_objects)
        sesh.commit()

    @classmethod
    def update_answers(cls, sesh, answers_data):
        """
        Документация метода
        """
        for item in answers_data:
            answer = sesh.query(Answers).filter(Answers.id == item["id"]).first()
            if answer:
                answer.answer = item["answer"]
                answer.question_id = item["question_id"]
                sesh.commit()
            else:
                raise ValueError(f"id {item["id"]} не найден для изменения.")

    @classmethod
    def delete_answers(cls, sesh, answers_id):
        """
        Документация метода
        """
        for item in answers_id:
            answer_to_delete = sesh.query(Answers).filter(Answers.id == item["id"]).one_or_none()
            if answer_to_delete is None:
                raise ValueError(f"id {item["id"]} не найден для удаления.")
            sesh.delete(answer_to_delete)
            answer_to_delete.delete_with_question(sesh)
        sesh.commit()

    @classmethod
    def get_answer(cls, sesh, answer_id):
        """
        Документация метода
        """
        answer_object = sesh.get(Answers, answer_id)
        if answer_object is None:
            raise ValueError(f"id {answer_id} не найден.")

        return answer_object

    @classmethod
    def create_answer(cls, sesh, answer_data):
        """
        Документация метода
        """
        pass

    @classmethod
    def update_answer(cls, sesh, answer_id, answer_data):
        """
        Документация метода
        """
        answer = sesh.query(Answers).filter(Answers.id == answer_id).first()
        if answer:
            answer.answer = answer_data["answer"]
            sesh.commit()
        else:
            raise ValueError(f"id {answer_id} не найден для изменения.")

    @classmethod
    def delete_answer(cls, sesh, answer_id):
        """
        Документация метода
        """
        answer_to_delete = sesh.query(Answers).filter(Answers.id == answer_id).one_or_none()
        if answer_to_delete is None:
            raise ValueError(f"id {answer_id} не найден для удаления.")
        sesh.delete(answer_to_delete)
        answer_to_delete.delete_with_question(sesh)
        sesh.commit()

    def delete_with_question(self, sesh):
        """
        Документация метода
        """
        if self.question:
            sesh.delete(self.question)
