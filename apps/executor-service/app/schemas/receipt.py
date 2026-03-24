from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

class ReceiptUpdate(BaseModel):
    paid_at: datetime | None = None
    tip: Decimal | None = None
    service: Decimal | None = None
    place_name: str | None = None
    status: str | None = None


class ReceiptOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    creator_id: int
    paid_at: datetime
    tip: Decimal
    service: Decimal
    place_name: str | None
    status: str
    created_at: datetime