"""
Документация модуля
"""

from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from app.models.initialize_db import Session
from app.models.question import Questions
from app.schemas.question import QuestionSchema, QuestionDeleteSchema


class QuestionsApi(Resource):
    """
    Документация класса
    """

    @staticmethod
    def get():
        """
        Документация метода
        """
        with Session() as se:
            questions = Questions.all_questions(se)
            schema = QuestionSchema(many=True)
            result = schema.dump(questions)
            return {"message": result}, 200

    @staticmethod
    def post():
        """
        Документация метода
        """
        data = request.get_json()

        if not isinstance(data, list):
            return {"error": "На вход ожидается список словарей с данными"}, 400

        schema = QuestionSchema(many=True)

        try:
            questions_data = schema.load(data)
            with Session() as se:
                Questions.add_questions(se, questions_data)
        except ValidationError as err:
            return {'errors': err.messages}, 422
        except ValueError as err:
            return {'errors': err.__str__()}, 400

        return {"message": "Данные добавлены"}, 200

    @staticmethod
    def put():
        """
        Документация метода
        """
        data = request.get_json()

        if not isinstance(data, list):
            return {"error": "На вход ожидается список словарей с данными"}, 400

        schema = QuestionSchema(many=True)

        try:
            questions_data = schema.load(data)
            with Session() as se:
                Questions.update_questions(se, questions_data)
        except ValidationError as err:
            return {'errors': err.messages}, 422
        except ValueError as err:
            return {'errors': err.__str__()}, 400

        return {"message": "Данные обновлены"}, 200

    @staticmethod
    def delete():
        """
        Документация метода
        """
        data = request.get_json()

        if not isinstance(data, list):
            return {"error": "На вход ожидается список словарей с данными"}, 400

        schema = QuestionDeleteSchema(many=True)

        try:
            questions_data = schema.load(data)
            with Session() as se:
                Questions.delete_questions(se, questions_data)
        except ValidationError as err:
            return {'errors': err.messages}, 422
        except ValueError as err:
            return {'errors': err.__str__()}, 400

        return {"message": "Данные удалены"}, 200


class QuestionApi(Resource):
    """
    Документация класса
    """

    @staticmethod
    def get(id):
        """
        Документация метода
        """
        try:
            with Session() as se:
                questions = Questions.get_question(se, id)
                schema = QuestionSchema()
                result = schema.dump(questions)
                return {"message": result}, 200
        except ValueError as err:
            return {'errors': err.__str__()}, 400

    @staticmethod
    def post(id):  # noqa
        """
        Документация метода
        """
        pass

        return {"error": "endpoint в разработке"}, 501

    @staticmethod
    def put(id):
        """
        Документация метода
        """
        data = request.get_json()

        if not isinstance(data, dict):
            return {"error": "На вход ожидается словарь с данными"}, 400

        schema = QuestionSchema()

        try:
            questions_data = schema.load(data)
            with Session() as se:
                Questions.update_question(se, id, questions_data)
        except ValidationError as err:
            return {'errors': err.messages}, 422
        except ValueError as err:
            return {'errors': err.__str__()}, 400

        return {"message": "Данные обновлены"}, 200

    @staticmethod
    def delete(id):
        """
        Документация метода
        """
        try:
            with Session() as se:
                Questions.delete_question(se, id)
        except ValueError as err:
            return {'errors': err.__str__()}, 400

        return {"message": "Данные удалены"}, 200
