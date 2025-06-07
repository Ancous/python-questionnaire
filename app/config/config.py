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
        data=session.get("data"),
        answer=session.get("answer"),
        message=session.get("message"),
        question=session.get("question"),
        statistic=session.get("statistic"),
        question_id=session.get("question_id"),
        sub_question=session.get("sub_question"),
        question_all=session.get("question_all"),
        authorization=bool(session.get('logged_in')),
    )
