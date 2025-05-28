"""
Документация модуля
"""

from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from app.models.answer import Answers
from app.models.initialize_db import Session

from app.schemas.answer import AnswerSchema, AnswerDeleteSchema


class AnswersApi(Resource):
    """
    Документация класса
    """

    @staticmethod
    def get():
        """
        Документация метода
        """
        with Session() as se:
            questions = Answers.all_answers(se)
            schema = AnswerSchema(many=True)
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

        schema = AnswerSchema(many=True)

        try:
            answer_data = schema.load(data)
            with Session() as se:
                Answers.add_answers(se, answer_data)
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

        schema = AnswerSchema(many=True)

        try:
            answer_data = schema.load(data)
            with Session() as se:
                Answers.update_answers(se, answer_data)
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

        schema = AnswerDeleteSchema(many=True)

        try:
            answer_data = schema.load(data)
            with Session() as se:
                Answers.delete_answers(se, answer_data)
        except ValidationError as err:
            return {'errors': err.messages}, 422
        except ValueError as err:
            return {'errors': err.__str__()}, 400

        return {"message": "Данные удалены"}, 200


class AnswerApi(Resource):
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
                answer = Answers.get_answer(se, id)
                schema = AnswerSchema()
                result = schema.dump(answer)
                return {"message": result}, 200
        except ValueError as err:
            return {'errors': err.__str__()}, 400

    @staticmethod
    def post(id):
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

        schema = AnswerSchema()

        try:
            answer_data = schema.load(data)
            with Session() as se:
                Answers.update_answer(se, id, answer_data)
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
                Answers.delete_answer(se, id)
        except ValueError as err:
            return {'errors': err.__str__()}, 400

        return {"message": "Данные удалены"}, 200
