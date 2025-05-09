from fastapi import APIRouter
from typing import Annotated

from schemas import STaskAdd
from repository import TaskRepository

router = APIRouter(
  prefix="/tasks"
)

@router.post("")
async def add_task(task: Annotated[STaskAdd, Depends()]):
  task_id = await TaskRepository.add_one(task)
  return {"ok": True, "task_id": task_id}

@router.get("")
async def get_home():
  tasks = await TaskRepository.find_all()
  retutn {"tasks": tasks}
