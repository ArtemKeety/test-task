from typing import Callable

from fastapi import HTTPException

from schemas import OrderCreate, OrderResponse, OrderUpdate
from repo import DishRepo, OrderRepo
from utils import Status, next_status


class OrderService:

    @staticmethod
    async def add(order: OrderCreate) -> int:
        """ При создании заказа проверять, что все указанные блюда существуют """
        dish = await DishRepo.get_all()
        dish_id_list = [i.id for i in dish] if dish else []

        if all(i in dish_id_list for i in order.dishes_ids):
            return await OrderRepo.add(order)
        else:
            raise HTTPException(status_code=404, detail="Не найдены блюда для заказа")


    @staticmethod
    async def get_all() -> list[OrderResponse]:
        return await OrderRepo.get_all()


    @staticmethod
    async def delete_by_id(id: int) -> Callable[[], int]:
        order = await OrderRepo.get_by_id(id)
        """ Заказ можно отменить только в статусе "в обработке". """
        if order and order.status.lower() == Status.first:
            return await OrderRepo.delete_by_id(id)
        else:
            raise HTTPException(status_code=500, detail=f"Заказа в стадии {order.status}, Его нельзя отменить")


    @staticmethod
    async def update_order(order: OrderUpdate) -> Callable[[], int]:
        order_old = await OrderRepo.get_by_id(order.id)
        if order and order.status.lower() == next_status(order_old.status):
            return await OrderRepo.update_order(order)
        else:
            raise HTTPException(status_code=500, detail="Изменение статуса должно быть последовательным")