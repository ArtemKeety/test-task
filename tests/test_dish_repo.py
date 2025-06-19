# tests/test_dish_repo.py

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.models import Model as Base, Dish
from app.schemas import DishCreate
from app.repo import DishRepo
from db import DataBase
from sqlalchemy.future import select


DATABASE_URL = DataBase.url
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="module", autouse=True)
async def prepare_db():
    # Используем DataBase.engine (у тебя он есть в db.py), например:
    from db import DataBase
    engine = DataBase.engine  # или create_async_engine(DataBase.url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio
async def test_add_dish():
    # Подготавливаем тестовое блюдо
    dish = DishCreate(name="Плов", description="Рис с мясом", price=300, category="Основное")

    # Добавляем блюдо через репозиторий
    dish_id = await DishRepo.add(dish)

    # Проверяем, что возвращаемый id является целым числом и больше нуля
    assert isinstance(dish_id, int)
    assert dish_id > 0

    # Получаем блюдо по ID и проверяем его данные
    async with DataBase.async_session() as db:
        result = await db.execute(select(Dish).where(Dish.id == dish_id))
        added_dish = result.scalars().first()

    assert added_dish is not None
    assert added_dish.name == dish.name
    assert added_dish.description == dish.description
    assert added_dish.price == dish.price
    assert added_dish.category == dish.category


@pytest.mark.asyncio
async def test_get_all_dishes():
    # Добавляем несколько блюд
    dish_1 = DishCreate(name="Плов", description="Рис с мясом", price=300, category="Основное")
    dish_2 = DishCreate(name="Шашлык", description="Мясо на углях", price=500, category="Основное блюдо")
    await DishRepo.add(dish_1)
    await DishRepo.add(dish_2)

    # Получаем все блюда
    dishes = await DishRepo.get_all()

    # Проверяем, что вернулся список блюд
    assert isinstance(dishes, list)
    assert len(dishes) >= 2  # Убедимся, что мы добавили хотя бы два блюда

    # Проверим наличие хотя бы одного блюда
    assert any(dish.name == "Плов" for dish in dishes)
    assert any(dish.name == "Шашлык" for dish in dishes)


@pytest.mark.asyncio
async def test_get_dish_by_id():
    # Добавляем блюдо
    dish = DishCreate(name="Плов", description="Рис с мясом", price=300, category="Основное")
    dish_id = await DishRepo.add(dish)

    # Получаем блюдо по ID
    found_dish = await DishRepo.get_by_id(dish_id)

    # Проверяем, что блюдо найдено и его данные совпадают с теми, что были добавлены
    assert found_dish is not None
    assert found_dish.id == dish_id
    assert found_dish.name == "Плов"
    assert found_dish.description == "Рис с мясом"
    assert found_dish.price == 300
    assert found_dish.category == "Основное"


@pytest.mark.asyncio
async def test_delete_dish():
    # Добавляем блюдо
    dish = DishCreate(name="Шашлык", description="Мясо на углях", price=500, category="Основное блюдо")
    dish_id = await DishRepo.add(dish)

    # Удаляем блюдо по ID
    deleted_count = await DishRepo.delete_by_id(dish_id)

    # Проверяем, что одно блюдо было удалено
    assert deleted_count == 1

    # Пытаемся получить удаленное блюдо
    deleted_dish = await DishRepo.get_by_id(dish_id)

    # Проверяем, что блюдо больше не существует
    assert deleted_dish is None