"""
Документация модуля
"""

from fastapi import APIRouter, Depends
from typing import Annotated

from schemas import STaskAdd, STask, STaskId
from repository import TaskRepository

router = APIRouter(
    prefix="/tasks",
    tags=["Таски"]
)


@router.post("")
async def add_task(task: Annotated[STaskAdd, Depends()]) -> STaskId:
    """
    Документация функции
    """
    task_id = await TaskRepository.add_one(task)
    return {"ok": True, "task_id": task_id}  # noqa


@router.get("")
async def get_home() -> list[STask]:
    """
    Документация функции
    """
    tasks = await TaskRepository.find_all()
    return tasks
