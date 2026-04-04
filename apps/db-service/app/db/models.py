from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum

from sqlalchemy import (
    Boolean,
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.database import Base


class ReceiptStatusEnum(str, Enum):
    PARSING = "parsing"
    DRAFT = "draft"
    ASSIGNED = "assigned"
    ARCHIVED = "archived"


class RoomStatusEnum(str, Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class PaidStatusEnum(str, Enum):
    NOT_PAID = "not paid"
    ON_REVIEW = "on review"
    PAID = "paid"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64))
    user_public_name: Mapped[str | None] = mapped_column(String(64))
    registered_at: Mapped[datetime] = mapped_column(nullable=False, default=lambda: datetime.now(timezone.utc))

    created_rooms: Mapped[list["Room"]] = relationship(back_populates="creator", foreign_keys="Room.creator_id")
    room_participations: Mapped[list["RoomParticipant"]] = relationship(back_populates="user")
    item_assignments: Mapped[list["ItemAssignment"]] = relationship(back_populates="user")

class Receipt(Base):
    __tablename__ = "receipts"

    id: Mapped[int] = mapped_column(primary_key=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT", onupdate="CASCADE"))
    paid_at: Mapped[datetime] = mapped_column()
    tip: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00"))
    service: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=Decimal("0.00"))
    place_name: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[ReceiptStatusEnum] = mapped_column(SQLEnum(ReceiptStatusEnum), default=ReceiptStatusEnum.PARSING)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=lambda: datetime.now(timezone.utc))

    creator: Mapped["User"] = relationship()
    rooms: Mapped[list["Room"]] = relationship(back_populates="receipt")
    items: Mapped[list["ReceiptItem"]] = relationship("ReceiptItem", back_populates="receipt", cascade="all, delete-orphan")


class Room(Base):
    __tablename__ = "rooms"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(255), nullable=False)
    public_key = mapped_column(String(6), unique=True, nullable=False)
    creator_id = mapped_column(Integer, ForeignKey("users.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    receipt_id = mapped_column(Integer, ForeignKey("receipts.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    status = mapped_column(SQLEnum(RoomStatusEnum), nullable=False, default=RoomStatusEnum.ACTIVE)
    payment_details = mapped_column(String(256), nullable=True)
    receipt_comment = mapped_column(String(256), nullable=True)
    created_at = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    is_active = mapped_column(Boolean, nullable=False, default=True)

    creator = relationship("User", back_populates="created_rooms", foreign_keys=[creator_id])
    receipt = relationship("Receipt", back_populates="rooms")
    participants = relationship("RoomParticipant", back_populates="room", cascade="all, delete-orphan")


class RoomParticipant(Base):
    __tablename__ = "room_participants"

    room_id = mapped_column(Integer, ForeignKey("rooms.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    joined_at = mapped_column(DateTime, default=datetime.utcnow)

    room = relationship("Room", back_populates="participants")
    user = relationship("User", back_populates="room_participations")


class ReceiptItem(Base):
    __tablename__ = "receipt_items"

    id = mapped_column(Integer, primary_key=True)
    receipt_id = mapped_column(Integer, ForeignKey("receipts.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    name = mapped_column(String(255), nullable=False)
    price = mapped_column(Numeric(10, 2), nullable=False)
    quantity = mapped_column(Numeric(10, 3), nullable=False, default=Decimal("1.000"))

    receipt = relationship("Receipt", back_populates="items")
    assignments = relationship("ItemAssignment", back_populates="item", cascade="all, delete-orphan")


class ItemAssignment(Base):
    __tablename__ = "item_assignments"

    item_id = mapped_column(Integer, ForeignKey("receipt_items.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    user_id = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    paid = mapped_column(SQLEnum(PaidStatusEnum), nullable=False, default=PaidStatusEnum.NOT_PAID)

    item = relationship("ReceiptItem", back_populates="assignments")
    user = relationship("User", back_populates="item_assignments")
