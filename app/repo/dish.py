
from app.schemas import DishCreate, DishResponse
from app.models import Dish
from .base import BaseRepo





class DishRepo(BaseRepo):
    add_form = DishCreate
    response_form = DishResponse
    orm = Dish

