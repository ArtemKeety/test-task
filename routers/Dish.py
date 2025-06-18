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