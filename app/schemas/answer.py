"""
Модуль схем для сериализации и валидации ответов.

Содержит схемы для создания, проверки и удаления ответов.
"""

from marshmallow import Schema, fields, ValidationError, validates

from app.models import Session
from app.models.answer import Answers
from app.models.question import Questions


class AnswerSchema(Schema):
    """
    Схема для сериализации и валидации объекта ответа.

    Arguments:
    id (fields.Integer): идентификатор ответа
    answer (fields.String): текст ответа (обязателен)
    question_id (fields.Integer): идентификатор вопроса (обязателен)
    """
    id = fields.Integer()
    answer = fields.String(required=True)
    question_id = fields.Integer(required=True)

    def __init__(self, *args, **kwargs) -> None:
        """
        Инициализация схемы ответа.
        """
        super().__init__(*args, **kwargs)
        self.question_ids = set()

    @validates("question_id")
    def validate_data(self, question_id: int, **kwargs) -> int:
        """
        Валидирует поле question_id: проверяет уникальность и существование вопроса.

        Parameters:
        question_id (int): идентификатор вопроса

        Return:
        question_id (int): идентификатор вопроса, если он валиден
        """
        if question_id in self.question_ids:
            raise ValidationError("question_id должен быть уникальным для каждого ответа.")
        self.question_ids.add(question_id)

        with Session() as se:
            if not se.query(Questions).filter_by(id=question_id).first():
                raise ValidationError(f"Вопроса с id {question_id} не существует.")
            if se.query(Answers).filter_by(question_id=question_id).first():
                raise ValidationError(f"Вопрос с id {question_id} уже привязан к ответу.")

        return question_id


class AnswerDeleteSchema(Schema):
    """
    Схема для удаления ответа по идентификатору.

    Arguments:
    id (fields.Integer): идентификатор ответа (обязателен)
    """
    id = fields.Integer(required=True)
