# tests/test_order_service.py

import pytest
from unittest.mock import MagicMock
from fastapi import HTTPException
from app.schemas import OrderCreate, OrderUpdate, OrderResponse
from app.repo import OrderRepo, DishRepo
from app.services import OrderService
from app.utils import Status


@pytest.fixture
def mock_order_repo():
    """Мокаем репозиторий OrderRepo для тестов"""
    mock_repo = MagicMock(spec=OrderRepo)
    OrderRepo.get_by_id = mock_repo.get_by_id
    OrderRepo.add = mock_repo.add
    OrderRepo.get_all = mock_repo.get_all
    OrderRepo.delete_by_id = mock_repo.delete_by_id
    OrderRepo.update_order = mock_repo.update_order
    return mock_repo


@pytest.fixture
def mock_dish_repo():
    """Мокаем репозиторий DishRepo для тестов"""
    mock_repo = MagicMock(spec=DishRepo)
    DishRepo.get_by_id = mock_repo.get_by_id
    return mock_repo


@pytest.mark.asyncio
async def test_add(mock_order_repo, mock_dish_repo):
    # Подготавливаем данные
    dish_1 = MagicMock(id=1, name="Плов")
    dish_2 = MagicMock(id=2, name="Шашлык")

    mock_dish_repo.get_by_id.side_effect = [dish_1, dish_2]  # Мокируем получение блюд по ID

    order_data = OrderCreate(
        customer_name="Иван Иванов",
        dishes_ids=[1, 2]  # Указываем ID существующих блюд
    )

    # Настроим мок репозитория, чтобы он возвращал id добавленного заказа
    mock_order_repo.add.return_value = 1

    # Выполняем метод
    result = await OrderService.add(order_data)

    # Проверяем, что заказ был добавлен
    assert result == 1
    mock_dish_repo.get_by_id.assert_any_call(1)  # Проверяем, что DishRepo.get_by_id был вызван для ID 1
    mock_dish_repo.get_by_id.assert_any_call(2)  # Проверяем, что DishRepo.get_by_id был вызван для ID 2
    mock_order_repo.add.assert_awaited_once_with(order_data)  # Проверяем, что метод был вызван с правильным аргументом


@pytest.mark.asyncio
async def test_add_order_with_nonexistent_dish(mock_order_repo, mock_dish_repo):
    # Подготавливаем данные
    dish_1 = MagicMock(id=1, name="Плов")

    mock_dish_repo.get_by_id.side_effect = [dish_1, None]  # Мокируем, что второе блюдо не найдено

    order_data = OrderCreate(
        customer_name="Иван Иванов",
        dishes_ids=[1, 999]  # Указываем ID несуществующего блюда
    )

    # Проверка, что выбрасывается HTTPException
    with pytest.raises(HTTPException):
        await OrderService.add(order_data)


@pytest.mark.asyncio
async def test_get_all(mock_order_repo):
    # Настроим мок для возвращаемых данных
    order_1 = MagicMock(id=1, customer_name="Иван Иванов")
    order_2 = MagicMock(id=2, customer_name="Петр Петров")

    mock_order_repo.get_all.return_value = [order_1, order_2]

    # Выполняем метод
    result = await OrderService.get_all()

    # Проверяем, что вернулся список заказов
    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0].customer_name == "Иван Иванов"
    assert result[1].customer_name == "Петр Петров"
    mock_order_repo.get_all.assert_awaited_once()  # Проверяем, что метод был вызван


@pytest.mark.asyncio
async def test_delete_by_id(mock_order_repo):
    # Подготавливаем данные
    order = MagicMock(id=1, status=Status.first)

    mock_order_repo.get_by_id.return_value = order
    mock_order_repo.delete_by_id.return_value = 1  # Возвращаем количество удаленных записей

    # Выполняем метод
    result = await OrderService.delete_by_id(1)

    # Проверяем, что удаление прошло успешно
    assert result == 1
    mock_order_repo.delete_by_id.assert_awaited_once_with(1)  # Проверяем, что метод был вызван с правильным ID


@pytest.mark.asyncio
async def test_delete_by_id_with_invalid_status(mock_order_repo):
    # Подготавливаем данные с неправильным статусом
    order = MagicMock(id=1, status=Status.second)  # Статус, который не позволяет удаление

    mock_order_repo.get_by_id.return_value = order

    # Проверка, что выбрасывается исключение при попытке удалить заказ с неправильным статусом
    with pytest.raises(HTTPException):
        await OrderService.delete_by_id(1)


@pytest.mark.asyncio
async def test_update_order(mock_order_repo):
    # Подготавливаем данные
    order = MagicMock(id=1, status=Status.first)
    mock_order_repo.get_by_id.return_value = order

    updated_order_data = OrderUpdate(
        id=1,
        status=Status.second  # Новый статус, последовательный
    )

    mock_order_repo.update_order.return_value = 1  # Возвращаем успешный результат обновления

    # Выполняем метод
    result = await OrderService.update_order(updated_order_data)

    # Проверяем, что обновление прошло успешно
    assert result == 1
    mock_order_repo.update_order.assert_awaited_once_with(updated_order_data)


@pytest.mark.asyncio
async def test_update_order_with_invalid_status(mock_order_repo):
    # Подготавливаем данные с неправильным статусом
    order = MagicMock(id=1, status=Status.second)
    mock_order_repo.get_by_id.return_value = order

    updated_order_data = OrderUpdate(
        id=1,
        status=Status.first  # Новый статус, но статус должен быть последовательным
    )

    # Проверка, что выбрасывается исключение при попытке обновить статус на несоответствующий
    with pytest.raises(HTTPException):
        await OrderService.update_order(updated_order_data)
