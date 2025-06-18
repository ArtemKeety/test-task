from fastapi import Depends, APIRouter
from services import OrderService
from schemas import OrderCreate, OrderUpdate

router = APIRouter()


@router.get("/orders/", response_model=list[OrderCreate])
async def get_orders():
    return await OrderService.get_all()


@router.post("/orders/", response_model=int)
async def create_order(order: OrderCreate):
    return await OrderService.add(order)


@router.delete("/orders/{id}", description="Отменить заказ")
async def delete_order(order_id: int):
    return await OrderService.delete_by_id(order_id)


@router.patch("/orders/{id}/status", response_model=int)
async def update_order(order: OrderUpdate = Depends()):
    return await OrderService.update_order(order)



