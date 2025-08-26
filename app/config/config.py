"""
Модуль конфигурации приложения.
Содержит переменные окружения, настройки подключения к БД и Redis, а также вспомогательные функции для авторизации.
"""

import os
import secrets
import re

from dotenv import load_dotenv
from flask import session

load_dotenv()

# POSTGRES_URL: str = "postgresql://root:1975@31.129.100.106:5432/python_interview"
# POSTGRES_URL: str = "postgresql://root:1975@127.0.0.1:5432/python_interview"
NUMBER_OF_QUESTIONS = 403
QUESTION_PATTERN: re.Pattern = re.compile(
    r"### (?P<number_question>\d+).\s+(?P<question>.*?)"
    r"\s+(?P<trash>&nbsp;\s*)*<small>\[Ответ](?P<link>.*)</small>",
)
ANSWER_LINK_PREFIX = "[Ответ]("
ANSWER_LINK_SUFFIX = ")"
IGNORE_LINE_PREFIXES = (
    "<div",
    "[Вернуться к вопросам]",
    "</div",
    "\n",
)
CODEBLOCK = "```"
POSTGRES_URL = (
    f"postgresql://"
    f"{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)
REDIS_URL = f"redis://" f"{os.getenv('REDIS_HOST')}:" f"{os.getenv('REDIS_PORT')}/0"
FLASK_SECRET_KEY = secrets.token_hex(16)


def inject_authorization() -> dict:
    """
    Формирует словарь с данными авторизации пользователя из сессии.

    Return:
    auth_data (dict): словарь с данными пользователя и статусом авторизации
    """
    return dict(
        user_id=session.get("user_id"),
        username=session.get("username"),
        statistic=session.get("statistic"),
        question_id=session.get("question_id"),
        question_all=session.get("question_all"),
        authorization=bool(session.get("logged_in") is True),
        number_questions_answered=session.get("number_questions_answered"),
    )
