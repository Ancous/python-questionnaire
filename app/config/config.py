"""
Документация модуля
"""

import os
import secrets

from dotenv import load_dotenv
from flask import session

load_dotenv()

POSTGRES_URL = (
    f"postgresql://"
    f"{os.getenv("DB_USER")}:"
    f"{os.getenv("DB_PASSWORD")}@"
    f"{os.getenv("DB_HOST")}:"
    f"{os.getenv("DB_PORT")}/"
    f"{os.getenv("DB_NAME")}"
)

REDIS_URL = (
    f"redis://"
    f"{os.getenv("REDIS_HOST")}:"
    f"{os.getenv("REDIS_PORT")}/0"
)

FLASK_SECRET_KEY = secrets.token_hex(16)


def inject_authorization():
    """
    Документация функции
    """
    return dict(
        user_id=session.get("user_id"),
        username=session.get("username"),
        statistic=session.get("statistic"),
        question_id=session.get("question_id"),
        question_all=session.get("question_all"),
        authorization=bool(session.get('logged_in') is True),
        number_questions_answered=session.get("number_questions_answered")
    )
