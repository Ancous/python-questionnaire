from pydantyc import BaseModel


class STaskAdd(BaseModel):
  name: str
  description: str | None

class STask(STaskAdd):
  id: int
