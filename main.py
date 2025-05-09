from fastapi import FastAPI
from typing import Annotated
from contextlib import asynccontextmanager

from database import delete_tables, create_tables
from schemas import STaskAdd

@asynccontextmanager
async def lifespan():
  await delete_tables()
  print("База очищена")
  await create_tables()
  print("База готова к работе")
  yield
  print("Выключение")

app = FastAPI(lifespan=lifespan)

tasks = list()

@app.post("/tasks")
async def add_task(task: Annotated[STaskAdd, Depends()]):
  tasks.append(task)
  return {"ok": True}

@app.get("/tasks")
def get_home():
  task = Task(name="Запиши это видео")
  retutn {"data": task}
