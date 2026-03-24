from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from decimal import Decimal
from dataclasses import dataclass

class ReceiptItem(BaseModel):
    """
    Сущность - позиция в чеке
    """
    name: str = Field(description="название позиции")
    price: float  = Field(description="стоимость позиции")
    quantity: float  = Field(default=1.0, description="количетсво позиции в чеке, либо ее вес, если стоимость зависит от веса")


class ResponseFormat(BaseModel):
    """Результат работы по запросу пользователя."""
    task: str = Field(description="Задача которую просил выполнить пользователь")
    made: bool = Field(default=True,
                       description="Достаточно ли текущей информации для выполнении задачи")
    error_message: str | None = Field(description="Сообщение о том, какую информацию необходимо предоставить, если текущей недостаточно")
    result: str = Field(description="Была ли задача успешно выполнена, если нет, то почему")


# app/agent/schemas.py
from dataclasses import dataclass
from app.clients.db_client import DBClient


@dataclass
class AgentContext:
    """Контекст, который прокидывается в tools агента."""
    db_client: DBClient
    receipt_id: str | None = None
    room_id: str | None = None
    user_id: str | None = None
