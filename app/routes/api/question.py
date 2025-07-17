"""
Модуль реализует API для работы с вопросами (Questions) через Flask-RESTful.
Содержит классы ресурсов для получения, добавления, обновления и удаления вопросов.
"""

from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from app.models.initialize_db import Session
from app.models.question import Questions
from app.schemas.question import QuestionSchema, QuestionDeleteSchema


class QuestionsApi(Resource):
    """
    Класс-ресурс для работы с коллекцией вопросов.
    """

    @staticmethod
    def get() -> tuple[dict, int]:
        """
        Получить все вопросы из базы данных.

        Return:
        message (dict): словарь с ключом 'message' и списком вопросов
        """
        with Session() as se:
            questions = Questions.all_questions(se)
            schema = QuestionSchema(many=True)
            result = schema.dump(questions)
            return {"message": result}, 200

    @staticmethod
    def post() -> tuple[dict, int]:
        """
        Добавить список вопросов в базу данных.

        Return:
        message (dict): словарь с сообщением об успехе или ошибке
        """
        data = request.get_json()

        if not isinstance(data, list):
            return {"error": "На вход ожидается список словарей с данными"}, 400

        schema = QuestionSchema(many=True)

        try:
            questions_data = schema.load(data)
            if not isinstance(questions_data, list):
                return {"error": "Ошибка валидации: ожидается список словарей"}, 400
            with Session() as se:
                Questions.add_questions(se, questions_data)
        except ValidationError as err:
            return {"errors": err.messages}, 422
        except ValueError as err:
            return {"errors": err.__str__()}, 400

        return {"message": "Данные добавлены"}, 200

    @staticmethod
    def put() -> tuple[dict, int]:
        """
        Обновить список вопросов в базе данных.

        Return:
        message (dict): словарь с сообщением об успехе или ошибке
        """
        data = request.get_json()

        if not isinstance(data, list):
            return {"error": "На вход ожидается список словарей с данными"}, 400

        schema = QuestionSchema(many=True)

        try:
            questions_data = schema.load(data)
            if not isinstance(questions_data, list):
                return {"error": "Ошибка валидации: ожидается список словарей"}, 400
            with Session() as se:
                Questions.update_questions(se, questions_data)
        except ValidationError as err:
            return {"errors": err.messages}, 422
        except ValueError as err:
            return {"errors": err.__str__()}, 400

        return {"message": "Данные обновлены"}, 200

    @staticmethod
    def delete() -> tuple[dict, int]:
        """
        Удалить список вопросов из базы данных.

        Return:
        message (dict): словарь с сообщением об успехе или ошибке
        """
        data = request.get_json()

        if not isinstance(data, list):
            return {"error": "На вход ожидается список словарей с данными"}, 400

        schema = QuestionDeleteSchema(many=True)

        try:
            questions_data = schema.load(data)
            if not isinstance(questions_data, list):
                return {"error": "Ошибка валидации: ожидается список словарей"}, 400
            with Session() as se:
                Questions.delete_questions(se, questions_data)
        except ValidationError as err:
            return {"errors": err.messages}, 422
        except ValueError as err:
            return {"errors": err.__str__()}, 400

        return {"message": "Данные удалены"}, 200


class QuestionApi(Resource):
    """
    Класс-ресурс для работы с отдельным вопросом.
    """

    @staticmethod
    def get(id: int) -> tuple[dict, int]:
        """
        Получить вопрос по id из базы данных.

        Parameters:
        id (int): идентификатор вопроса

        Return:
        message (dict): словарь с вопросом или ошибкой
        """
        try:
            with Session() as se:
                questions = Questions.get_question(se, id)
                schema = QuestionSchema()
                result = schema.dump(questions)
                return {"message": result}, 200
        except ValueError as err:
            return {"errors": err.__str__()}, 400

    @staticmethod
    def post(id: int) -> tuple[dict, int]:
        """
        Заглушка для POST по id (не реализовано).

        Parameters:
        id (int): идентификатор вопроса

        Return:
        error (dict): словарь с сообщением об ошибке
        """
        pass

        return {"error": "endpoint в разработке"}, 501

    @staticmethod
    def put(id: int) -> tuple[dict, int]:
        """
        Обновить вопрос по id в базе данных.

        Parameters:
        id (int): идентификатор вопроса

        Return:
        message (dict): словарь с сообщением об успехе или ошибке
        """
        data = request.get_json()

        if not isinstance(data, dict):
            return {"error": "На вход ожидается словарь с данными"}, 400

        schema = QuestionSchema()

        try:
            questions_data = schema.load(data)
            if not isinstance(questions_data, dict):
                return {"error": "Ошибка валидации: ожидается словарь"}, 400
            with Session() as se:
                Questions.update_question(se, id, questions_data)
        except ValidationError as err:
            return {"errors": err.messages}, 422
        except ValueError as err:
            return {"errors": err.__str__()}, 400

        return {"message": "Данные обновлены"}, 200

    @staticmethod
    def delete(id: int) -> tuple[dict, int]:
        """
        Удалить вопрос по id из базы данных.

        Parameters:
        id (int): идентификатор вопроса

        Return:
        message (dict): словарь с сообщением об успехе или ошибке
        """
        try:
            with Session() as se:
                Questions.delete_question(se, id)
        except ValueError as err:
            return {"errors": err.__str__()}, 400

        return {"message": "Данные удалены"}, 200
