"""
Модуль для работы с API БД.
Реализует клиента для работы с БД.
Клиент реализует функции обновления, изменения, получения и создания записей.
"""


import httpx
from typing import Any
from app.core.config import settings
from app.core.logger import get_logger
from app.schemas.receipt_item import ReceiptItemCreate, ReceiptItemUpdate, ReceiptItemOut
from app.schemas.receipt import ReceiptUpdate

logger = get_logger(__name__)
    
class DBClient:
    """Клиент для взаимодействия с API БД"""

    def __init__(self, base_url: str | None = None):
        self.base_url = base_url if base_url else settings.database_api_url
        logger.info(
            f"Initialized client for DB API"
        )

    async def _request(
            self,
            method: str,
            path: str,
            **kwargs
    ) -> dict[str, Any] | None:
        """
        Базовый метод для всех запросов
        Args:
            method: метод HTTP запроса
            path: путь запроса
            **kwargs: словарь оставшихся именованных аргументов
        Returns:
            словарь - ответ от API
        """
        url = f"{self.base_url}{path}"
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.request(method=method, url=url, **kwargs)
                logger.info(f"Response to DB API, method: {method}")
                response.raise_for_status()

                if response.status_code == 204 or not response.text:
                    return None

                return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"DB API error: {e.response.status_code}: {e.response.text}")
            raise
        except httpx.RequestError as e:
            logger.error(f"DB API connection error: {e}")
            raise

    """
    Методы для изменения информации о позициях
    """
    async def add_item(
            self,
            payload: ReceiptItemCreate
    ) -> dict[str, Any]:
        """
        Метод для добавления позиции
        Args:
            payload: информация о новой позиции
        Returns:
            словарь, элементы которого: поля новой позиции
        """

        data = payload.model_dump(exclude_none=True)

        return await self._request(
            "POST",
            "/items",
            json=data,
        )

    async def update_item(
            self,
            item_id: int,
            payload: ReceiptItemUpdate
    ) -> dict[str, Any]:
        """
        Метод для обновления позиции
        Args:
            item_id: id позиции
            payload: информация для обновления позиции
        Returns:
            словарь, элементы которого: поля обновленной позиции
        """
        data = payload.model_dump(exclude_unset=True)
        return await self._request(
            "PATCH",
            f"/items/{item_id}",
            json=data
        )

    async def get_item(
            self,
            item_id: int
    ) -> dict[str, Any]:
        """Метод для получения позиции
        Args:
            item_id: id позиции
        Returns:
            словарь, элементы которого: поля найденной позиции
        """
        return await self._request(
            "GET",
            f"/items/{item_id}",
        )

    async def delete_item(
            self,
            item_id: int
    ) -> None:
        """Метод для удаления позиции
        Args:
            item_id: id позиции
        Returns:
            None: ничего не возвращает при успехе, либо выбрасывает исключение
        """
        await self._request(
            "DELETE",
            f"/items/{item_id}"
        )


    """
    Методы для изменения информации о чеках
    """
    async def update_receipt(
            self,
            receipt_id: int,
            payload: ReceiptUpdate
    ) -> dict[str, Any]:
        """
        Метод для обновления чека
        Args:
            receipt_id: id чека
            payload: информация для обновления чека
        Returns:
            словарь, элементы которого: поля обновленного чека
        """
        data = payload.model_dump(exclude_unset=True)
        return await self._request(
            "PATCH",
            f"/receipts/{receipt_id}",
            json=data
        )