"""
Документация модуля
"""

from marshmallow import Schema, fields


class QuestionSchema(Schema):
    id = fields.Integer()
    question = fields.String(required=True)
    sub_question = fields.String(required=True, allow_none=True)


class QuestionDeleteSchema(Schema):
    id = fields.Integer(required=True)
