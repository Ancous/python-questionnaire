"""
Документация модуля
"""

from flask_restful import Resource
from sqlalchemy import MetaData, inspect, Table
from sqlalchemy.exc import InternalError

from app.models.initialize_db import engine
from app.utils.tables_info import inspector_tables


class TablesApi(Resource):
    """
    Документация класса
    """

    @staticmethod
    def get():
        """
        Документация функции
        """
        inspector = inspect(engine)
        table_names = inspector.get_table_names()
        result = inspector_tables(inspector, table_names)

        return {"database": result}, 200

    @staticmethod
    def post():
        """
        Документация функции
        """
        pass

        return {"error": "endpoint в разработке"}, 501

    @staticmethod
    def put():
        """
        Документация функции
        """
        pass

        return {"error": "endpoint в разработке"}, 501

    @staticmethod
    def delete():
        """
        Документация функции
        """
        metadata = MetaData()
        metadata.reflect(engine)
        metadata.drop_all(engine)

        return {"message": "Все таблицы успешно удалены."}, 200


class TableApi(Resource):
    """
    Документация класса
    """

    @staticmethod
    def get(name):
        """
        Документация функции
        """
        inspector = inspect(engine)
        if name not in inspector.get_table_names():
            return {"error": f"Таблицы {name} не существует."}, 404

        inspector = inspect(engine)
        tables_names = inspector.get_table_names()
        result = inspector_tables(inspector, tables_names, name)

        return {"table": result}, 200

    @staticmethod
    def post(name):  # noqa
        """
        Документация функции
        """
        pass

        return {"error": "endpoint в разработке"}, 501

    @staticmethod
    def put(name):  # noqa
        """
        Документация функции
        """
        pass

        return {"error": "endpoint в разработке"}, 501

    @staticmethod
    def delete(name):
        """
        Документация функции
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
                return {"error": f"Таблица {name} не может быть удалена из за связей в таблицах."}, 409

        return {"message": f"Таблица {name} удалена."}, 200
