from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

class ChatRequest(BaseModel):
    user_message: str
    user_id: str
    receipt_id: str


class CommandResult(BaseModel):
    id: str
    data: str


class Transcription(BaseModel):
    text: str
    language: str
# ──────────────────────────────
# User
# ──────────────────────────────

class UserCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, str_min_length=1)

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
    id: str
    paid_at: datetime


class ReceiptUpdate(BaseModel):
    paid_at: datetime | None = None


class ReceiptOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    paid_at: datetime


# ──────────────────────────────
# Room
# ──────────────────────────────

class RoomCreate(BaseModel):
    id: str
    name: str
    creator_id: str
    receipt_id: str | None = None


class RoomUpdate(BaseModel):
    name: str | None = None
    receipt_id: str | None = None
    is_active: bool | None = None


class RoomOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    creator_id: str
    receipt_id: str | None
    created_at: datetime
    is_active: bool


# ──────────────────────────────
# RoomParticipant
# ──────────────────────────────

class ParticipantOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    room_id: str
    user_id: str
    username: str
    user_public_name: str | None
    joined_at: datetime | None


# ──────────────────────────────
# ReceiptItem
# ──────────────────────────────

class ReceiptItemCreate(BaseModel):
    id: str
    receipt_id: str
    name: str
    price: Decimal
    quantity: Decimal = Decimal("1.000")


class ReceiptItemUpdate(BaseModel):
    name: str | None = None
    price: Decimal | None = None
    quantity: Decimal | None = None


class ReceiptItemOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    receipt_id: str
    name: str
    price: Decimal
    quantity: Decimal


# ──────────────────────────────
# ItemAssignment
# ──────────────────────────────

class AssignmentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    item_id: str
    user_id: str
