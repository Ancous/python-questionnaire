"""
Документация модуля
"""

from flask import jsonify, Blueprint
from sqlalchemy import MetaData

from models.models import engine

api_tables_bp = Blueprint(
    "tables",
    __name__,
    url_prefix="/api/tables"
)


@api_tables_bp.route("/", methods=["DELETE"])
def tables():
    """
    Документация функции
    """
    metadata = MetaData()
    metadata.reflect(bind=engine)
    metadata.drop_all(bind=engine)

    return jsonify({"message": "Все таблицы успешно удалены."}), 200
