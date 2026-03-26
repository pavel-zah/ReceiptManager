"""
Модуль для работы с API БД.
Реализует клиента для работы с БД.
Клиент реализует функции обновления, изменения, получения и создания записей.
"""


import httpx
from typing import Any, List
from pydantic import TypeAdapter
from app.core.config import settings
from app.core.logger import get_logger
from app.schemas.receipt_item import ReceiptItemCreate, ReceiptItemUpdate, ReceiptItemOut
from app.schemas.receipt import ReceiptUpdate

logger = get_logger(__name__)

receipt_items_adapter = TypeAdapter(List[ReceiptItemCreate])

    
class DBClient:
    """Клиент для взаимодействия с API БД"""

    def __init__(self, base_url: str | None = None):
        self.base_url = base_url if base_url else settings.database_api_url

        self.session = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=10.0
        )

        logger.info(f"Initialized client for DB API with base_url: {self.base_url}")

    async def close(self):
        """
        Метод для закрытия соединения при остановке приложения
        """
        await self.session.aclose()
        logger.info(f"DB API client session with base_url: {self.base_url} was closed")

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
        try:
            response = await self.session.request(method=method, url=path, **kwargs)
            logger.info(f"Response to DB API, method: {method}, path: {path}, status: {response.status_code}")
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
    async def add_items(
            self,
            item_id: int,
            payload: List[ReceiptItemCreate]
    ) -> dict[str, Any]:
        """
        Метод для добавления позиций
        Args:
            item_id: id позиции
            payload: список с информацией о новых позициях
        Returns:
            список, с информацией о добавленных позициях
        """

        data = receipt_items_adapter.dump_python(payload, exclude_none=True)

        return await self._request(
            "POST",
            f"/items/{item_id}",
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