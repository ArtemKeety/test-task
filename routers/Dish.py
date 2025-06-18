from fastapi import Depends, APIRouter
from services import DishService
from schemas import DishCreate

router = APIRouter()


@router.get("/dishes/")
async def get_dish():
    return await DishService.get_all()


@router.post("/dishes/")
async def add_dish(dish: DishCreate):
    return await DishService.add(dish)


@router.delete("/dishes/{dish_id}")
async def remove_dish(dish_id: int):
    return await DishService.delete_by_id(dish_id)
