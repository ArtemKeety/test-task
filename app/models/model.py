from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from .base import Model
from app.utils import Status


order_dish_table = Table(
    "order_dish",
    Model.metadata,
    Column("order_id", Integer, ForeignKey("orders.id", ondelete="CASCADE"), primary_key=True),
    Column("dish_id", Integer, ForeignKey("dish.id", ondelete="CASCADE"), primary_key=True),
)


class Dish(Model):
    __tablename__ = 'dish'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))
    price: Mapped[float] = mapped_column()
    category: Mapped[str] = mapped_column(String(255))

    orders: Mapped[list["Order"]] = relationship(
        "Order",
        secondary=order_dish_table,
        back_populates="dishes",
        passive_deletes=True,
    )


class Order(Model):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_name: Mapped[str] = mapped_column(String(255))  # ✅
    order_time: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    status: Mapped[str] = mapped_column(String(255), default=Status.first.value)  # ✅

    dishes: Mapped[list["Dish"]] = relationship(
        "Dish",
        secondary=order_dish_table,
        back_populates="orders",
        passive_deletes=True,
    )
