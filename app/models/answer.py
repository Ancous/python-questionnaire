"""
Модуль содержит модель Answers для хранения правильных ответов на вопросы.
"""

from typing import Sequence
from sqlalchemy.orm import Mapped, mapped_column, relationship, Session
from sqlalchemy import Integer, String, ForeignKey, select

from app.models import BaseModel


class Answers(BaseModel):
    """
    Класс правильного ответа на вопрос.

    Arguments:
    id (int): уникальный идентификатор ответа
    answer (str): текст правильного ответа
    question_id (int): внешний ключ на вопрос (Questions)
    question (relationship): связь с вопросом, к которому относится ответ
    """

    __tablename__ = "answers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    answer: Mapped[str] = mapped_column(String, nullable=False)
    question_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("questions.id"), unique=True, nullable=False
    )

    question = relationship("Questions", back_populates="answer", uselist=False)

    def __repr__(self) -> str:
        """
        Представление объекта ответа в виде строки.

        Return:
        str: строковое представление ответа
        """
        return f"<Answer(id={self.id}, answer={self.answer}, question_id={self.question_id})>"

    @classmethod
    def all_answers(cls, sesh: Session) -> Sequence["Answers"]:
        """
        Получить все объекты ответов.

        Parameters:
        sesh (Session): сессия SQLAlchemy

        Return:
        all_answers_objects (list[Answers]): список всех ответов
        """
        stmt = select(cls)
        all_answers_objects = sesh.scalars(stmt).all()
        return all_answers_objects

    @classmethod
    def add_answers(cls, sesh: Session, answers_data: list[dict]) -> None:
        """
        Добавить несколько ответов в базу данных.

        Parameters:
        sesh (Session): сессия SQLAlchemy
        answers_data (list[dict]): данные для добавления
        """
        answers_objects = [cls(answer=item["answer"]) for item in answers_data]
        sesh.add_all(answers_objects)
        sesh.commit()

    @classmethod
    def update_answers(cls, sesh: Session, answers_data: list[dict]) -> None:
        """
        Обновить несколько ответов в базе данных.

        Parameters:
        sesh (Session): сессия SQLAlchemy
        answers_data (list[dict]): данные для обновления
        """
        for item in answers_data:
            stmt = select(cls).where(cls.id == item["id"])
            answer = sesh.scalars(stmt).one()
            if answer:
                answer.answer = item["answer"]
                answer.question_id = item["question_id"]
                sesh.commit()
            else:
                raise ValueError(f"id {item['id']} не найден для изменения.")

    @classmethod
    def delete_answers(cls, sesh: Session, answers_id: list[dict]) -> None:
        """
        Удалить несколько ответов по id.

        Parameters:
        sesh (Session): сессия SQLAlchemy
        answers_id (list[dict]): список id для удаления
        """

        for item in answers_id:
            stmt = select(cls).where(cls.id == item["id"])
            answer_to_delete = sesh.scalars(stmt).first()
            if answer_to_delete is None:
                raise ValueError(f"id {item['id']} не найден для удаления.")
            answer_to_delete.delete_with_question(sesh)
            sesh.delete(answer_to_delete)
        sesh.commit()

    @classmethod
    def get_answer(cls, sesh: Session, answer_id: int) -> "Answers":
        """
        Получить объект ответа по id.

        Parameters:
        sesh (Session): сессия SQLAlchemy
        answer_id (int): id ответа

        Return:
        answer_object (Answers): найденный объект ответа
        """
        answer_object = sesh.get(cls, answer_id)
        if answer_object is None:
            raise ValueError(f"id {answer_id} не найден.")
        return answer_object

    @classmethod
    def create_answer(cls, sesh: Session, answer_data: dict) -> None:
        """
        Создать новый ответ (реализация не указана).

        Parameters:
        sesh (Session): сессия SQLAlchemy
        answer_data (dict): данные для создания
        """
        pass

    @classmethod
    def update_answer(cls, sesh: Session, answer_id: int, answer_data: dict) -> None:
        """
        Обновить ответ по id.

        Parameters:
        sesh (Session): сессия SQLAlchemy
        answer_id (int): id ответа
        answer_data (dict): новые данные
        """
        stmt = select(cls).where(cls.id == answer_id)
        answer = sesh.scalars(stmt).one()
        if answer:
            answer.answer = answer_data["answer"]
            sesh.commit()
        else:
            raise ValueError(f"id {answer_id} не найден для изменения.")

    @classmethod
    def delete_answer(cls, sesh: Session, answer_id: int) -> None:
        """
        Удалить ответ по id.

        Parameters:
        sesh (Session): сессия SQLAlchemy
        answer_id (int): id ответа
        """
        stmt = select(cls).where(cls.id == answer_id)
        answer_to_delete = sesh.scalars(stmt).one()
        if answer_to_delete is None:
            raise ValueError(f"id {answer_id} не найден для удаления.")
        sesh.delete(answer_to_delete)
        answer_to_delete.delete_with_question(sesh)
        sesh.commit()

    @classmethod
    def answer_by_question_id(cls, sesh: Session, id_question: int) -> "Answers":
        """
        Получить ответ по id вопроса.

        Parameters:
        sesh (Session): сессия SQLAlchemy
        id_question (int): id вопроса

        Return:
        answer_obj (Answers): найденный объект ответа
        """
        stmt = select(cls).where(cls.question_id == id_question)
        answer_obj = sesh.scalars(stmt).one()
        return answer_obj

    def delete_with_question(self, sesh: Session) -> None:
        """
        Удалить связанный вопрос вместе с ответом, если он существует.

        Parameters:
        sesh (Session): сессия SQLAlchemy
        """
        if self.question:
            sesh.delete(self.question)
