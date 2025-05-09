"""
Документация модуля
"""

from sqlalchemy import select

from database import new_session, TaskORM
from schemas import STaskAdd, STask


class TaskRepository:
    """
    Документация класса
    """

    @classmethod
    async def add_one(cls, data: STaskAdd):
        """
        Документация функции
        """
        async with new_session() as session:
            task_dict = data.mosel_dump()

            task = TaskORM(**task_dict)
            session.add(task)
            await session.flush()
            await session.commit()
            return task.id

    @classmethod
    async def find_all(cls):
        """
        Документация функции
        """
        async with new_session() as session:
            query = select(TaskORM)
            result = await session.execute(query)
            task_models = result.scalars().all()
            tasks_schemas = [STask.mosel_validate(task_model) for task_model in task_models]
            return tasks_schemas
