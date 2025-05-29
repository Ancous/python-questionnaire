"""
Документация модуля
"""

import os
import secrets

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = (
    f"postgresql://"
    f"{os.getenv("DB_USER")}:"
    f"{os.getenv("DB_PASSWORD")}@"
    f"{os.getenv("DB_HOST")}:"
    f"{os.getenv("DB_PORT")}/"
    f"{os.getenv("DB_NAME")}"
)

FLASK_SECRET_KEY = secrets.token_hex(16)
