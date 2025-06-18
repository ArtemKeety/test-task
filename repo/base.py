from functools import wraps
from sqlalchemy.exc import SQLAlchemyError
from db import DataBase
from fastapi import HTTPException

def handler(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):

        async with DataBase.async_session() as db:
            try:
                return await func(*args, **kwargs, db=db)
            except SQLAlchemyError as e:
                raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {func.__name__} {e}") from e

    return wrapper