from typing import Callable

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from .base import BaseRepo, handler
from app.models import Order, Dish
from app.schemas import OrderCreate, OrderResponse, OrderIncomplete, OrderUpdate


class OrderRepo(BaseRepo):
    add_form = OrderCreate
    response_form = OrderIncomplete
    orm = Order
    response_form_all = OrderResponse
    update_form = OrderUpdate

    @classmethod
    @handler
    async def add(cls, order_data: type(add_form), db: AsyncSession) -> int:
        dishes = (await db.execute(select(Dish).where(Dish.id.in_(order_data.dishes_ids)))).scalars().all()
        new_order = Order(
            customer_name=order_data.customer_name,
            #status=order_data.status,
            dishes=dishes
        )
        db.add(new_order)
        await db.commit()
        return new_order.id

    @classmethod
    @handler
    async def get_all(cls, db: AsyncSession) -> list[type(response_form_all)]:
        result = await db.execute(select(Order).options(selectinload(Order.dishes)))
        results = result.scalars().all()
        return [OrderResponse.model_validate(i) for i in results]

    @classmethod
    @handler
    async def update_order(cls, order: type(update_form), db: AsyncSession) -> Callable[[], int]:
        up = update(cls.orm).where(cls.orm.id == order.id).values(**order.__dict__)
        result = await db.execute(up)
        await db.commit()
        return result.rowcount
