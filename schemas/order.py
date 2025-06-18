from .base import Model
from datetime import datetime
from typing import List, Optional
from .dish import DishResponse
from utils import Status


class OrderUpdate(Model):
    id: int
    status: Status


class OrderCreate(Model):
    customer_name: str
    dishes_ids: List[int]
    #status: Optional[str] = "в обработке"
    #status: Status = Status.first


class OrderIncomplete(Model):
    id: int
    customer_name: str
    order_time: datetime
    status: str


class OrderResponse(OrderIncomplete):
    dishes: List[DishResponse]
