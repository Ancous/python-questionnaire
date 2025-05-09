from fastapi import FastAPI
from typing import Annotated
from pydantic import BaseModel
from contextlib import asynccontextmanager

from database import delete_tables, create_tables

@asynccontextmanager
async def lifespan():
  await delete_tables()
  print("База очищена")
  await create_tables()
  print("База готова к работе")
  yield
  print("Выключение")

app = FastAPI(lifespan=lifespan)

class STaskAdd(BaseModel):
  name: str
  description: str | None

class STask(STaskAdd):
  id: int

tasks = list()

@app.post("/tasks")
async def add_task(task: Annotated[STaskAdd, Depends()]):
  tasks.append(task)
  return {"ok": True}

@app.get("/tasks")
def get_home():
  task = Task(name="Запиши это видео")
  retutn {"data": task}
