from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum as SQLEnum,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import relationship
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

    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False)
    user_public_name = Column(String(64), nullable=True)
    registered_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    created_rooms = relationship("Room", back_populates="creator", foreign_keys="Room.creator_id")
    room_participations = relationship("RoomParticipant", back_populates="user")
    item_assignments = relationship("ItemAssignment", back_populates="user")


class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True)
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    paid_at = Column(DateTime, nullable=False)
    tip = Column(Numeric(10, 2), nullable=False, default=Decimal("0.00"))
    service = Column(Numeric(10, 2), nullable=False, default=Decimal("0.00"))
    place_name = Column(String(255), nullable=True)
    status = Column(SQLEnum(ReceiptStatusEnum), nullable=False, default=ReceiptStatusEnum.PARSING)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    creator = relationship("User")
    rooms = relationship("Room", back_populates="receipt")
    items = relationship("ReceiptItem", back_populates="receipt", cascade="all, delete-orphan")


class Room(Base):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    public_key = Column(String(6), unique=True, nullable=False)
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    receipt_id = Column(Integer, ForeignKey("receipts.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    status = Column(SQLEnum(RoomStatusEnum), nullable=False, default=RoomStatusEnum.ACTIVE)
    payment_details = Column(String(256), nullable=True)
    receipt_comment = Column(String(256), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    is_active = Column(Boolean, nullable=False, default=True)

    creator = relationship("User", back_populates="created_rooms", foreign_keys=[creator_id])
    receipt = relationship("Receipt", back_populates="rooms")
    participants = relationship("RoomParticipant", back_populates="room", cascade="all, delete-orphan")


class RoomParticipant(Base):
    __tablename__ = "room_participants"

    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    joined_at = Column(DateTime, default=datetime.utcnow)

    room = relationship("Room", back_populates="participants")
    user = relationship("User", back_populates="room_participations")


class ReceiptItem(Base):
    __tablename__ = "receipt_items"

    id = Column(Integer, primary_key=True)
    receipt_id = Column(Integer, ForeignKey("receipts.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Numeric(10, 3), nullable=False, default=Decimal("1.000"))

    receipt = relationship("Receipt", back_populates="items")
    assignments = relationship("ItemAssignment", back_populates="item", cascade="all, delete-orphan")


class ItemAssignment(Base):
    __tablename__ = "item_assignments"

    item_id = Column(Integer, ForeignKey("receipt_items.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    paid = Column(SQLEnum(PaidStatusEnum), nullable=False, default=PaidStatusEnum.NOT_PAID)

    item = relationship("ReceiptItem", back_populates="assignments")
    user = relationship("User", back_populates="item_assignments")
