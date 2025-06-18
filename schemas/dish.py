from .base import Model

# class DishRequest(Model):
#     name: str = "Пицца Маргарита"
#     description: str = "Пицца Маргарита - очень вкусная, есть тесто, сыр, колбаса"
#     price: float = 49.90
#     category: str = "Основное блюдо"
#
#
# class DishResponse(DishRequest):
#     id: int

from pydantic import Field
from typing import Optional


class DishBase(Model):
    name: str = Field(..., example="Пицца Маргарита")
    description: str = Field(..., example="Пицца с сыром, тестом и колбасой")
    price: float = Field(..., example=49.90, gt=0)
    category: str = Field(..., example="Основное блюдо")


class DishCreate(DishBase):
    pass


class DishUpdate(Model):
    id: int
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None


class DishResponse(DishBase):
    id: int
