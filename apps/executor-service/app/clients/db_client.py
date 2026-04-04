"""
Модуль для работы с API БД.
Реализует клиента для работы с БД.
Клиент реализует функции обновления, изменения, получения и создания записей.
"""


import httpx
from typing import Any, List
from app.core.config import settings
from app.core.logger import get_logger
from app.schemas.receipt_item import ReceiptItemCreate, ReceiptItemUpdate, ReceiptItemOut, ReceiptItemBatchOut
from app.schemas.receipt import ReceiptUpdate
from fastapi.encoders import jsonable_encoder


logger = get_logger(__name__)

    
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
            receipt_id: int,
            payload: List[ReceiptItemCreate]
    ) -> ReceiptItemBatchOut:
        """
        Метод для добавления позиций
        Args:
            receipt_id: id чека для добавления новых позиций
            payload: список с информацией о новых позициях
        Returns:
            Валидированный объект, с информацией о добавленных позициях
        """

        data = jsonable_encoder(
            [item.model_dump(exclude_none=True) for item in payload]
        )

        response_data = await self._request(
            "POST",
            f"/items/{receipt_id}",
            json=data,
        )

        items_count = len(response_data.get("items", []))
        logger.info(f"Added {items_count} items to receipt {receipt_id}")

        return ReceiptItemBatchOut.model_validate(response_data)


    async def update_item(
            self,
            item_id: int,
            payload: ReceiptItemUpdate
    ) -> ReceiptItemOut:
        """
        Метод для обновления позиции
        Args:
            item_id: id позиции
            payload: информация для обновления позиции
        Returns:
            Валидированный объект с информацией об обновленной позиции
        """
        data = jsonable_encoder(
            payload.model_dump(exclude_unset=True)
        )

        response_data = await self._request(
            "PATCH",
            f"/items/{item_id}",
            json=data
        )

        return ReceiptItemOut.model_validate(response_data)


    async def get_item(
            self,
            item_id: int
    ) -> ReceiptItemOut | None:
        """Метод для получения позиции
        Args:
            item_id: id позиции
        Returns:
            Валидированный объект с информацией об искомой позиции. None, если объект не найден
        """
        try:
            response_data =  await self._request(
                "GET",
                f"/items/{item_id}",
            )

            return ReceiptItemOut.model_validate(response_data)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                logger.info(f"Item with id {item_id} not found in DB.")
                return None
            raise


    async def get_receipt_items(
            self,
            receipt_id: int
    ) -> ReceiptItemBatchOut | None:
        """Метод для получения позиции
        Args:
            receipt_id: id чека
        Returns:
            Валидированный объект с информацией о блюдах в чеке. None, если чек не найден
        """
        try:
            response_data =  await self._request(
                "GET",
                f"/receipts/{receipt_id}/items",
            )

            items = response_data.get("items", {})
            if items:
                return None
            else:
                return ReceiptItemBatchOut.model_validate(items)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                logger.info(f"Receipt with id {receipt_id} not found in DB.")
                return None
            raise

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