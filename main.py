"""
Документация модуля
"""

from fastapi import FastAPI
from typing import AsyncGenerator
from contextlib import asynccontextmanager

from database import delete_table, create_table
from router import router as tasks_router


@asynccontextmanager
async def lifespan() -> AsyncGenerator[None, None]:
    """
    Документация функции
    """
    await delete_table()
    print("База очищена")
    await create_table()
    print("База готова к работе")
    yield
    print("Выключение")


app = FastAPI(lifespan=lifespan)  # noqa
app.include_router(tasks_router)
