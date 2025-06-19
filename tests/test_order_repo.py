import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, selectinload

from app.models import Model as Base, Order, Dish
from app.schemas import OrderCreate, OrderResponse, OrderUpdate
from app.repo import OrderRepo
from db import DataBase

DATABASE_URL = DataBase.url
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="module", autouse=True)
async def prepare_db():
    # Создаем все таблицы в базе данных
    async with AsyncSessionLocal() as db:
        from app.models import Model as base
        await db.execute(select(Dish))  # Убедимся, что таблицы есть
        base.metadata.create_all(bind=db.bind)
    yield
    # Удаляем таблицы после тестов
    async with AsyncSessionLocal() as db:
        from app.models import Base
        Base.metadata.drop_all(bind=db.bind)


@pytest.mark.asyncio
async def test_add_order():
    # Создаем тестовые блюда
    dish_1 = Dish(name="Плов", description="Рис с мясом", price=300, category="Основное")
    dish_2 = Dish(name="Шашлык", description="Мясо на углях", price=500, category="Основное блюдо")

    # Добавляем блюда в БД
    async with AsyncSessionLocal() as db:
        db.add(dish_1)
        db.add(dish_2)
        await db.commit()

    # Подготавливаем тестовое заказ
    order_data = OrderCreate(
        customer_name="Иван Иванов",
        dishes_ids=[dish_1.id, dish_2.id]
    )

    # Добавляем заказ
    order_id = await OrderRepo.add(order_data)

    # Проверяем, что заказ добавлен
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(Order).options(selectinload(Order.dishes)).where(Order.id == order_id))
        added_order = result.scalars().first()

    assert added_order is not None
    assert added_order.customer_name == order_data.customer_name
    assert len(added_order.dishes) == 2  # Должно быть два блюда в заказе


@pytest.mark.asyncio
async def test_get_all_orders():
    # Добавляем несколько заказов
    dish_1 = Dish(name="Плов", description="Рис с мясом", price=300, category="Основное")
    dish_2 = Dish(name="Шашлык", description="Мясо на углях", price=500, category="Основное блюдо")

    async with AsyncSessionLocal() as db:
        db.add(dish_1)
        db.add(dish_2)
        await db.commit()

    order_data_1 = OrderCreate(
        customer_name="Иван Иванов",
        dishes_ids=[dish_1.id]
    )
    order_data_2 = OrderCreate(
        customer_name="Петр Петров",
        dishes_ids=[dish_2.id]
    )

    #async with AsyncSessionLocal() as db:
    await OrderRepo.add(order_data_1)
    await OrderRepo.add(order_data_2)

    # Получаем все заказы

    orders = await OrderRepo.get_all()

    # Проверяем, что вернулся список заказов
    assert isinstance(orders, list)
    assert len(orders) >= 2  # Убедимся, что мы добавили хотя бы два заказа

    # Проверим наличие хотя бы одного заказа
    assert any(order.customer_name == "Иван Иванов" for order in orders)
    assert any(order.customer_name == "Петр Петров" for order in orders)


@pytest.mark.asyncio
async def test_get_order_by_id():
    # Добавляем заказ
    dish_1 = Dish(name="Плов", description="Рис с мясом", price=300, category="Основное")

    async with AsyncSessionLocal() as db:
        db.add(dish_1)
        await db.commit()

    order_data = OrderCreate(
        customer_name="Иван Иванов",
        dishes_ids=[dish_1.id]
    )


    order_id = await OrderRepo.add(order_data)

    # Получаем заказ по ID
    found_order = await OrderRepo.get_by_id(order_id)

    # Проверяем, что заказ найден и его данные совпадают с теми, что были добавлены
    assert found_order is not None
    assert found_order.id == order_id
    assert found_order.customer_name == "Иван Иванов"


@pytest.mark.asyncio
async def test_update_order():
    # Добавляем заказ
    dish_1 = Dish(name="Плов", description="Рис с мясом", price=300, category="Основное")

    async with AsyncSessionLocal() as db:
        db.add(dish_1)
        await db.commit()

    order_data = OrderCreate(
        customer_name="Иван Иванов",
        dishes_ids=[dish_1.id],
    )


    order_id = await OrderRepo.add(order_data)

    # Обновляем заказ
    updated_order_data = OrderUpdate(
        id=order_id,
        status="готовится",
    )

    updated_count = await OrderRepo.update_order(updated_order_data)

    # Проверяем, что обновление прошло успешно
    assert updated_count == 1

    # Получаем обновленный заказ
    found_order = await OrderRepo.get_by_id(order_id)

    # Проверяем, что данные обновлены
    assert found_order is not None
    assert found_order.status == "готовится"


@pytest.mark.asyncio
async def test_delete_order():
    # Добавляем заказ
    dish_1 = Dish(name="Плов", description="Рис с мясом", price=300, category="Основное")

    async with AsyncSessionLocal() as db:
        db.add(dish_1)
        await db.commit()

    order_data = OrderCreate(
        customer_name="Иван Иванов",
        dishes_ids=[dish_1.id]
    )

    order_id = await OrderRepo.add(order_data)

    # Удаляем заказ

    deleted_count = await OrderRepo.delete_by_id(order_id)

    # Проверяем, что заказ был удален
    assert deleted_count == 1

    # Пытаемся получить удаленный заказ
    deleted_order = await OrderRepo.get_by_id(order_id)

    # Проверяем, что заказа больше нет
    assert deleted_order is None