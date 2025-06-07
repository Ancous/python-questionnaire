"""
Документация модуля
"""

from sqlalchemy import event, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config.config import POSTGRES_URL


class Base(DeclarativeBase):
    """
    Документация класса
    """
    pass


class BaseModel(Base):
    __abstract__ = True

    @classmethod
    def __declare_last__(cls):
        """
        Документация метода
        """

        @event.listens_for(cls, 'before_insert')
        def validate_id(mapper, connection, target):  # noqa
            """
            Документация метода
            """
            if target.id is not None:
                raise ValueError("Запись id вручную запрещена.")


engine = create_engine(POSTGRES_URL)
Session = sessionmaker(engine)
