"""
Модуль реализует API для работы с ответами (Answers) через Flask-RESTful.
Содержит классы ресурсов для получения, добавления, обновления и удаления ответов.
"""

from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from collections.abc import Mapping, Sequence

from app.models.answer import Answers
from app.models.initialize_db import Session

from app.schemas.answer import AnswerSchema, AnswerDeleteSchema


class AnswersApi(Resource):
    """
    Ресурс для работы с коллекцией ответов.
    """

    @staticmethod
    def get() -> tuple[dict, int]:
        """
        Получить все ответы.

        Return:
        message (dict): словарь с ключом 'message' и списком ответов
        """
        with Session() as se:
            questions = Answers.all_answers(se)
            schema = AnswerSchema(many=True)
            result = schema.dump(questions)
            return {"message": result}, 200

    @staticmethod
    def post() -> tuple[dict, int]:
        """
        Добавить список ответов.

        Return:
        message (dict): словарь с сообщением об успехе или ошибке
        """
        data = request.get_json()

        if not isinstance(data, list):
            return {"error": "На вход ожидается список словарей с данными"}, 400

        schema = AnswerSchema(many=True)

        try:
            answer_data = schema.load(data)
            if not isinstance(answer_data, list):
                return {"error": "Ошибка валидации: ожидается список словарей"}, 400
            with Session() as se:
                Answers.add_answers(se, answer_data)
        except ValidationError as err:
            return {"errors": err.messages}, 422
        except ValueError as err:
            return {"errors": err.__str__()}, 400

        return {"message": "Данные добавлены"}, 200

    @staticmethod
    def put() -> tuple[dict, int]:
        """
        Обновить список ответов.

        Return:
        message (dict): словарь с сообщением об успехе или ошибке
        """
        data = request.get_json()

        if not isinstance(data, list):
            return {"error": "На вход ожидается список словарей с данными"}, 400

        schema = AnswerSchema(many=True)

        try:
            answer_data = schema.load(data)
            if not isinstance(answer_data, list):
                return {"error": "Ошибка валидации: ожидается список словарей"}, 400
            with Session() as se:
                Answers.update_answers(se, answer_data)
        except ValidationError as err:
            return {"errors": err.messages}, 422
        except ValueError as err:
            return {"errors": err.__str__()}, 400

        return {"message": "Данные обновлены"}, 200

    @staticmethod
    def delete() -> tuple[dict, int]:
        """
        Удалить список ответов.

        Return:
        message (dict): словарь с сообщением об успехе или ошибке
        """
        data = request.get_json()

        if not isinstance(data, list):
            return {"error": "На вход ожидается список словарей с данными"}, 400

        schema = AnswerDeleteSchema(many=True)

        try:
            answer_data = schema.load(data)
            if not isinstance(answer_data, list):
                return {"error": "Ошибка валидации: ожидается список словарей"}, 400
            with Session() as se:
                Answers.delete_answers(se, answer_data)
        except ValidationError as err:
            return {"errors": err.messages}, 422
        except ValueError as err:
            return {"errors": err.__str__()}, 400

        return {"message": "Данные удалены"}, 200


class AnswerApi(Resource):
    """
    Ресурс для работы с отдельным ответом.
    """

    @staticmethod
    def get(id: int) -> tuple[dict, int]:
        """
        Получить ответ по id.

        Parameters:
        id (int): идентификатор ответа

        Return:
        message (dict): словарь с ответом или ошибкой
        """
        try:
            with Session() as se:
                answer = Answers.get_answer(se, id)
                schema = AnswerSchema()
                result = schema.dump(answer)
                return {"message": result}, 200
        except ValueError as err:
            return {"errors": err.__str__()}, 400

    @staticmethod
    def post(id: int) -> tuple[dict, int]:  # noqa
        """
        Заглушка для POST по id (не реализовано).

        Parameters:
        id (int): идентификатор ответа

        Return:
        error (dict): словарь с сообщением об ошибке
        """
        pass

        return {"error": "endpoint в разработке"}, 501

    @staticmethod
    def put(id: int) -> tuple[dict, int]:
        """
        Обновить ответ по id.

        Parameters:
        id (int): идентификатор ответа

        Return:
        message (dict): словарь с сообщением об успехе или ошибке
        """
        data = request.get_json()

        if not isinstance(data, dict):
            return {"error": "На вход ожидается словарь с данными"}, 400

        schema = AnswerSchema()

        try:
            answer_data = schema.load(data)
            if not isinstance(answer_data, dict):
                return {"error": "Ошибка валидации: ожидается словарь"}, 400
            with Session() as se:
                Answers.update_answer(se, id, answer_data)
        except ValidationError as err:
            return {"errors": err.messages}, 422
        except ValueError as err:
            return {"errors": err.__str__()}, 400

        return {"message": "Данные обновлены"}, 200

    @staticmethod
    def delete(id: int) -> tuple[dict, int]:
        """
        Удалить ответ по id.

        Parameters:
        id (int): идентификатор ответа

        Return:
        message (dict): словарь с сообщением об успехе или ошибке
        """
        try:
            with Session() as se:
                Answers.delete_answer(se, id)
        except ValueError as err:
            return {"errors": err.__str__()}, 400

        return {"message": "Данные удалены"}, 200
