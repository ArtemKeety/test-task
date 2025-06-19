from fastapi import APIRouter
from app.services import DishService
from app.schemas import DishCreate, DishResponse

router = APIRouter()


@router.get("/dishes/", response_model=list[DishResponse])
async def get_dish():
    return await DishService.get_all()


@router.post("/dishes/", response_model=int)
async def add_dish(dish: DishCreate):
    return await DishService.add(dish)


@router.delete("/dishes/{id}", response_model=int)
async def remove_dish(dish_id: int):
    return await DishService.delete_by_id(dish_id)
