"""
Модуль реализует API для работы с базой данных через Flask-RESTful.
Содержит классы ресурсов для получения информации о таблицах и управления ими.
"""

from flask_restful import Resource
from sqlalchemy import MetaData, inspect, Table
from sqlalchemy.exc import InternalError

from app.models.initialize_db import engine
from app.utils.tables_info import inspector_tables


class TablesApi(Resource):
    """
    Класс-ресурс для работы со всеми таблицами базы данных.
    """

    @staticmethod
    def get() -> tuple[dict, int]:
        """
        Получить список всех таблиц и их структуру.

        Return:
        database (dict): информация о таблицах базы данных
        """
        inspector = inspect(engine)
        table_names = inspector.get_table_names()
        result = inspector_tables(inspector, table_names)

        return {"database": result}, 200

    @staticmethod
    def post() -> tuple[dict, int]:
        """
        Заглушка для POST (не реализовано).

        Return:
        error (dict): словарь с сообщением об ошибке
        """
        pass

        return {"error": "endpoint в разработке"}, 501

    @staticmethod
    def put() -> tuple[dict, int]:
        """
        Заглушка для PUT (не реализовано).

        Return:
        error (dict): словарь с сообщением об ошибке
        """
        pass

        return {"error": "endpoint в разработке"}, 501

    @staticmethod
    def delete() -> tuple[dict, int]:
        """
        Удалить все таблицы из базы данных.

        Return:
        message (dict): сообщение об успешном удалении
        """
        metadata = MetaData()
        metadata.reflect(engine)
        metadata.drop_all(engine)

        return {"message": "Все таблицы успешно удалены."}, 200


class TableApi(Resource):
    """
    Класс-ресурс для работы с отдельной таблицей базы данных.
    """

    @staticmethod
    def get(name: str) -> tuple[dict, int]:
        """
        Получить структуру и данные конкретной таблицы.

        Parameters:
        name (str): имя таблицы

        Return:
        table (dict): информация о таблице или сообщение об ошибке
        """
        inspector = inspect(engine)
        if name not in inspector.get_table_names():
            return {"error": f"Таблицы {name} не существует."}, 404

        inspector = inspect(engine)
        tables_names = inspector.get_table_names()
        result = inspector_tables(inspector, tables_names, name)

        return {"table": result}, 200

    @staticmethod
    def post(name: str) -> tuple[dict, int]:
        """
        Заглушка для POST по имени таблицы (не реализовано).

        Parameters:
        name (str): имя таблицы

        Return:
        error (dict): словарь с сообщением об ошибке
        """
        pass

        return {"error": "endpoint в разработке"}, 501

    @staticmethod
    def put(name: str) -> tuple[dict, int]:
        """
        Заглушка для PUT по имени таблицы (не реализовано).

        Parameters:
        name (str): имя таблицы

        Return:
        error (dict): словарь с сообщением об ошибке
        """
        pass

        return {"error": "endpoint в разработке"}, 501

    @staticmethod
    def delete(name: str) -> tuple[dict, int]:
        """
        Удалить таблицу по имени из базы данных.

        Parameters:
        name (str): имя таблицы

        Return:
        message (dict): сообщение об успешном удалении или ошибке
        """
        inspector = inspect(engine)
        if name not in inspector.get_table_names():
            return {"error": f"Таблицы {name} не существует."}, 404

        metadata = MetaData()
        table = Table(name, metadata, autoload_with=engine)
        try:
            table.drop(engine)
        except InternalError as exe:
            if "CASCADE" in exe.__str__():
                return {
                    "error": f"Таблица {name} не может быть удалена из за связей в таблицах."
                }, 409

        return {"message": f"Таблица {name} удалена."}, 200
