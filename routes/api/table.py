"""
Документация модуля
"""

from flask import jsonify, Blueprint
from sqlalchemy import MetaData

from models.models import engine

api_tables_bp = Blueprint(
    "tables",
    __name__,
    url_prefix="/api/table"
)


@api_tables_bp.route("/", methods=["GET"])
def tables_get():
    """
    Документация функции
    """
    ...

    return ..., 200


@api_tables_bp.route("/", methods=["POST"])
def tables_post():
    """
    Документация функции
    """
    ...

    return ..., 200


@api_tables_bp.route("/", methods=["PUT"])
def tables_put():
    """
    Документация функции
    """
    ...

    return ..., 200


@api_tables_bp.route("/", methods=["DELETE"])
def tables_delete():
    """
    Документация функции
    """
    metadata = MetaData()
    metadata.reflect(bind=engine)
    metadata.drop_all(bind=engine)

    return jsonify({"message": "Все таблицы успешно удалены."}), 200
