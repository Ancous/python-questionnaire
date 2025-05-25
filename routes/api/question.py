"""
Документация модуля
"""
import json

from flask import Blueprint, jsonify

from models.models import Session, Questions

api_questions_bp = Blueprint(
    "questions",
    __name__,
    url_prefix="/api/question"
)

api_question_bp = Blueprint(
    "question_id",
    __name__,
    url_prefix="/api/question/<int:id>"
)


@api_questions_bp.route("/", methods=["GET"])
def questions_get():
    """
    Документация функции
    """
    with Session() as se:
        result = Questions.search_questions(se)
        print(type(result))
        print(result)
    return jsonify({"task_group": result}), 200


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
    ...

    return ..., 200


@api_questions_bp.route("/", methods=["DELETE"])
def questions_delete():
    """
    Документация функции
    """
    ...

    return ..., 200


@api_question_bp.route("/", methods=["GET"])
def question_get(id):
    """
    Документация функции
    """
    ...

    return ..., 200


@api_question_bp.route("/", methods=["POST"])
def question_post(id):
    """
    Документация функции
    """
    ...

    return ..., 200


@api_question_bp.route("/", methods=["PUT"])
def question_put(id):
    """
    Документация функции
    """
    ...

    return ..., 200


@api_question_bp.route("/", methods=["DELETE"])
def question_delete(id):
    """
    Документация функции
    """
    ...

    return ..., 200
