from sqlalchemy import ForeignKey, Column, ForeignKeyConstraint, Integer, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from .base import Model


class Dish(Model):
    __tablename__ = 'dish'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[float]
    category: Mapped[str]

