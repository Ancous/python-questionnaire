"""
Документация модуля
"""

from sqlalchemy import Column, String, Integer

from app.models import BaseModel


class Users(BaseModel):
    """
    Документация класса
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
