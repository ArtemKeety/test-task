from typing import Callable

from schemas import DishCreate, DishResponse
from repo import DishRepo


class DishService:

    @classmethod
    async def get_all(cls) -> list[DishResponse]:
        return await DishRepo.get_all()

    @classmethod
    async def add(cls, dish: DishCreate) -> int:
        return await DishRepo.add(dish)

    @classmethod
    async def delete_by_id(cls, dish_id: int) -> Callable[[], int]:
        return await DishRepo.delete_by_id(dish_id)
