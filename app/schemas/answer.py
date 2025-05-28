"""
Документация модуля
"""

from marshmallow import Schema, fields, ValidationError, validates

from app.models import Session
from app.models.answer import Answers
from app.models.question import Questions


class AnswerSchema(Schema):
    id = fields.Integer()
    answer = fields.String(required=True)
    question_id = fields.Integer(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.question_ids = set()

    @validates("question_id")
    def validate_data(self, question_id, **kwargs):  # noqa
        """
        Документация метода
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
    id = fields.Integer(required=True)
