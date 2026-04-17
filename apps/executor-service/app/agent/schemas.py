from pydantic import BaseModel, Field
from typing import List
from typing_extensions import TypedDict, Annotated
from dataclasses import dataclass, field
from app.clients.db_client import DBClient
from app.schemas.receipt_item import ReceiptItemCreate, ReceiptItemUpdate, ReceiptItemBatchOut
from decimal import Decimal
import operator

# ===============
# Receipt schemas
# ===============
class ReceiptItemCreateSchema(BaseModel):
    """
    Сущность для создания позиции в чеке
    """
    name: str = Field(description="название позиции")
    price: float  = Field(description="стоимость позиции")
    quantity: float  = Field(default=1.0,
                             description="количетсво позиции в чеке, либо ее вес, если стоимость зависит от веса")

    def to_db_model(self) -> ReceiptItemCreate:
        return ReceiptItemCreate(
            name=self.name,
            price=Decimal(str(self.price)),
            quantity=Decimal(str(self.quantity))
        )

class ReceiptItemUpdateSchema(BaseModel):
    """
    Сущность для обновления данных позиции в чеке
    """
    name: str | None = Field(description="название позиции")
    price: float | None = Field(description="стоимость позиции")
    quantity: float | None = Field(default=1.0,
                            description="количетсво позиции в чеке, либо ее вес, если стоимость зависит от веса")

    def to_db_update(self) -> ReceiptItemUpdate:
        update_data = self.model_dump(exclude_unset=True)

        if "price" in update_data and update_data["price"] is not None:
            update_data["price"] = Decimal(str(update_data["price"]))
        if "quantity" in update_data and update_data["quantity"] is not None:
            update_data["quantity"] = Decimal(str(update_data["quantity"]))

        return ReceiptItemUpdate(**update_data)


class ReceiptItemBatchCreateSchema(BaseModel):
    """
    Сущность с информацией о позициях для добавления в чек позициях
    """
    items: List[ReceiptItemCreateSchema] = Field(description="список позиций для добавления в чек")


class ReceiptItemOutSchema(BaseModel):
    """
    Сущность - позиция в чеке
    """
    id: int = Field(description="Номер позиции в чеке")
    name: str = Field(description="название позиции")
    price: float  = Field(description="стоимость позиции")
    quantity: float  = Field(default=1.0,
                             description="количество позиции в чеке, либо ее вес, если стоимость зависит от веса")


class ReceiptItemBatchOutSchema(BaseModel):
    """
    Сущность с информацией о добавленных в чек позициях
    """
    items: List[ReceiptItemOutSchema] = Field(description="список добавленных позиций")


# ====================
# Agent Context Schema
# ====================

class AgentRoomState(TypedDict):
    """
    Контекст, который прокидывается в tools агента.
    """
    messages: Annotated[list, operator.add]
    # id_mapping: dict
    command: str
    answer: str
    params: dict | None
    error: str | None
    receipt_updated: bool
    added_items: ReceiptItemBatchOut

    # receipt_id: str | None = None
    # room_id: str | None = None
    # user_id: str | None = None

# =====================
# Agent Response Schema
# =====================


class ResponseFormatSchema(BaseModel):
    """
    Результат работы по запросу пользователя.
    """
    task: str = Field(description="Задача которую просил выполнить пользователь")
    made: bool = Field(default=True,
                       description="Достаточно ли текущей информации для выполнении задачи")
    error_message: str | None = Field(description="Сообщение о том, какую информацию необходимо предоставить, если текущей недостаточно")
    result: str = Field(description="Была ли задача успешно выполнена, если нет, то почему")
