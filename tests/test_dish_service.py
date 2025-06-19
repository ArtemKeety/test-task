# tests/test_dish_service.py

import pytest
from unittest.mock import MagicMock
from app.schemas import DishCreate, DishResponse
from app.services import DishService  # Импортируем сервис DishService
from app.repo import DishRepo


@pytest.fixture
def mock_dish_repo():
    """Мокаем репозиторий DishRepo для тестов"""
    mock_repo = MagicMock(spec=DishRepo)
    DishRepo.get_all = mock_repo.get_all
    DishRepo.add = mock_repo.add
    DishRepo.delete_by_id = mock_repo.delete_by_id
    return mock_repo


@pytest.mark.asyncio
async def test_get_all(mock_dish_repo):
    # Подготавливаем данные
    dish_1 = DishResponse(id=1, name="Плов", description="Рис с мясом", price=300, category="Основное")
    dish_2 = DishResponse(id=2, name="Шашлык", description="Мясо на углях", price=500, category="Основное блюдо")

    # Настроим мок репозитория, чтобы он возвращал эти блюда
    mock_dish_repo.get_all.return_value = [dish_1, dish_2]

    # Выполняем метод
    result = await DishService.get_all()

    # Проверяем, что результат — это список с двумя блюдами
    assert len(result) == 2
    assert result[0].name == "Плов"
    assert result[1].name == "Шашлык"
    mock_dish_repo.get_all.assert_awaited_once()  # Проверяем, что метод был вызван


@pytest.mark.asyncio
async def test_add(mock_dish_repo):
    # Подготавливаем данные
    dish = DishCreate(name="Плов", description="Рис с мясом", price=300, category="Основное")

    # Настроим мок репозитория, чтобы он возвращал id добавленного блюда
    mock_dish_repo.add.return_value = 1

    # Выполняем метод
    result = await DishService.add(dish)

    # Проверяем, что метод вернул правильный id
    assert result == 1
    mock_dish_repo.add.assert_awaited_once_with(dish)  # Проверяем, что метод был вызван с правильным аргументом


@pytest.mark.asyncio
async def test_delete_by_id(mock_dish_repo):
    # Подготавливаем данные
    dish_id = 1

    # Настроим мок репозитория, чтобы он возвращал количество удаленных блюд
    mock_dish_repo.delete_by_id.return_value = 1

    # Выполняем метод
    result = await DishService.delete_by_id(dish_id)

    # Проверяем, что метод вернул количество удаленных блюд
    assert result == 1
    mock_dish_repo.delete_by_id.assert_awaited_once_with(dish_id)  # Проверяем, что метод был вызван с правильным id
