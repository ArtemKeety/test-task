from functools import wraps

from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Callable
from db import DataBase
from fastapi import HTTPException


def handler(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):

        async with DataBase.async_session() as db:
            try:
                return await func(*args, **kwargs, db=db)
            except SQLAlchemyError as e:
                await db.rollback()
                raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {func.__name__} {e}") from e

    return wrapper


class BaseRepo:
    add_form = None
    response_form = None
    orm = None

    @classmethod
    @handler
    async def add(cls, dish: type(add_form), db: AsyncSession) -> int:
        new = cls.orm(**dish.model_dump())
        db.add(new)
        await db.flush()
        await db.commit()
        return new.id

    @classmethod
    @handler
    async def get_all(cls, db: AsyncSession) -> list[type(response_form)]:
        data = select(cls.orm)
        result = await db.execute(data)
        results = result.scalars().all()
        return [cls.response_form.model_validate(item) for item in results]

    @classmethod
    @handler
    async def delete_by_id(cls, object_id: int, db: AsyncSession) -> Callable[[], int]:
        dl = delete(cls.orm).where(cls.orm.id == object_id)
        result = await db.execute(dl)
        await db.commit()
        return result.rowcount
