"""
Модуль схем для сериализации и валидации вопросов.
Содержит схемы для создания, проверки и удаления вопросов.
"""

from marshmallow import Schema, fields


class QuestionSchema(Schema):
    """
    Схема для сериализации и валидации объекта вопроса.

    Arguments:
    id (fields.Integer): идентификатор вопроса
    question (fields.String): текст вопроса (обязателен)
    sub_question (fields.String): под-вопрос (обязателен, может быть None)
    """

    id = fields.Integer()
    question = fields.String(required=True)
    sub_question = fields.String(required=True, allow_none=True)


class QuestionDeleteSchema(Schema):
    """
    Схема для удаления вопроса по идентификатору.

    Arguments:
    id (fields.Integer): идентификатор вопроса (обязателен)
    """

    id = fields.Integer(required=True)
