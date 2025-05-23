"""
Документация модуля
"""

from flask import jsonify, Blueprint

from models.models import Session, Questions
from utils.data_processing import parse_question_file

api_questions_bp = Blueprint(
    "questions",
    __name__,
    url_prefix="/api/question"
)


@api_questions_bp.route("/", methods=["GET"])
def questions_get():
    """
    Документация функции
    """
    ...

    return ..., 200


@api_questions_bp.route("/", methods=["POST"])
def questions_post():
    """
    Документация функции
    """
    ...

    return ..., 200


@api_questions_bp.route("/", methods=["PUT"])
def questions_put():
    """
    Документация функции
    """
    with Session() as se:
        add_list = list()
        for data in parse_question_file():
            new_user = Questions(id=data[0], questions=data[1], add_question=data[3], answer=data[2])
            add_list.append(new_user)
        se.add_all(add_list)
        se.commit()

    return jsonify({"message": "Таблица с вопросами обновлена"}), 200


@api_questions_bp.route("/", methods=["DELETE"])
def questions_delete():
    """
    Документация функции
    """
    ...

    return ..., 200
