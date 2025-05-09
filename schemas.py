"""
Документация модуля
"""

from pydantic import BaseModel


class STaskAdd(BaseModel):
    """
    Документация класса
    """
    name: str
    description: str | None


class STask(STaskAdd):
    """
    Документация класса
    """
    id: int


class STaskId(BaseModel):
    """
    Документация класса
    """
    ok: bool = True
    task_id: int
