srom sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_async_engine("sqlite+aiosqlite:///tasks.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)

class Model(DeclarativeBase):
  pass

class TaskORM(Model):
  __tablename__ = "tasks"

id: Mapped[int] = mapped_column(primery_key=True)
name:  Mapped[int]
description: Mapped[int | None]

async def create_table():
  async with engine.begin() as conn:
    await conn.run_sync(Model.metedata.create_all)


async def delete_table():
  async with engine.begin() as conn:
    await conn.run_sync(Model.metedata.drop_all)
