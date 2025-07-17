"""
Модуль инициализации моделей базы данных.
"""

from sqlalchemy import event, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config.config import POSTGRES_URL


class Base(DeclarativeBase):
    """
    Базовый класс для всех моделей SQLAlchemy.
    Используется для декларативного описания моделей.
    """

    pass


class BaseModel(Base):
    """
    Абстрактный базовый класс для всех моделей.
    """

    __abstract__ = True

    @classmethod
    def __declare_last__(cls) -> None:
        """
        Добавляет валидацию id перед вставкой записи.
        """

        @event.listens_for(cls, "before_insert")
        def validate_id(mapper, connection, target) -> None:  # noqa
            """
            Запрещает ручную вставку id.
            """
            if target.id is not None:
                raise ValueError("Запись id вручную запрещена.")


engine = create_engine(POSTGRES_URL)
Session = sessionmaker(engine)
