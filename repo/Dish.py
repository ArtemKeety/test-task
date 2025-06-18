from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import DishCreate, DishResponse
from models import Dish
from .base import handler





class DishRepo:

    @classmethod
    @handler
    async def add(cls, dish: DishCreate, db: AsyncSession) -> int:
        new = Dish(**dish.model_dump())
        db.add(new)
        await db.flush()
        await db.commit()
        return new.id


    @classmethod
    @handler
    async def get_all(cls, db: AsyncSession) -> list[DishResponse]:
        data = select(Dish)
        result = await db.execute(data)
        results = result.scalars().all()
        return [DishResponse.model_validate(item) for item in results]
