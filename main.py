from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

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
