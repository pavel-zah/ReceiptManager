from datetime import datetime
from decimal import Decimal
from typing import List

from pydantic import BaseModel, ConfigDict


# ──────────────────────────────
# User
# ──────────────────────────────

class UserCreate(BaseModel):
    username: str
    user_public_name: str | None = None


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    username: str
    user_public_name: str | None
    registered_at: datetime


# ──────────────────────────────
# Receipt
# ──────────────────────────────

class ReceiptCreate(BaseModel):
    creator_id: int
    paid_at: datetime | None = None
    tip: Decimal = Decimal("0.00")
    service: Decimal = Decimal("0.00")
    place_name: str | None = None
    status: str = "parsing"


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


# ──────────────────────────────
# Room
# ──────────────────────────────

class RoomCreate(BaseModel):
    name: str
    public_key: str
    creator_id: int
    receipt_id: int
    status: str = "active"
    payment_details: str | None = None
    receipt_comment: str | None = None


class RoomUpdate(BaseModel):
    name: str | None = None
    receipt_id: int | None = None
    status: str | None = None
    payment_details: str | None = None
    receipt_comment: str | None = None
    is_active: bool | None = None


class RoomOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    public_key: str
    creator_id: int
    receipt_id: int
    status: str
    payment_details: str | None
    receipt_comment: str | None
    created_at: datetime
    is_active: bool


# ──────────────────────────────
# RoomParticipant
# ──────────────────────────────

class ParticipantOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    room_id: int
    user_id: int
    joined_at: datetime | None


# ──────────────────────────────
# ReceiptItem
# ──────────────────────────────

class ReceiptItemCreate(BaseModel):
    name: str
    price: Decimal
    quantity: Decimal = Decimal("1.000")

class ReceiptItemUpdate(BaseModel):
    name: str | None = None
    price: Decimal | None = None
    quantity: Decimal | None = None

class ReceiptItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    receipt_id: int
    name: str
    price: Decimal
    quantity: Decimal

# ──────────────────────────────
# ItemAssignment
# ──────────────────────────────

class AssignmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    item_id: int
    user_id: int
    paid: str
