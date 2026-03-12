from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Numeric,
    String,
)
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String(255), primary_key=True)
    username = Column(String(255), nullable=False)
    registered_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    created_rooms = relationship("Room", back_populates="creator", foreign_keys="Room.creator_id")
    room_participations = relationship("RoomParticipant", back_populates="user")
    item_assignments = relationship("ItemAssignment", back_populates="user")


class Receipt(Base):
    __tablename__ = "receipts"

    id = Column(String(255), primary_key=True)
    paid_at = Column(DateTime, nullable=False)
    tip = Column(Numeric(10, 2), nullable=False, default=Decimal("0.00"))
    service = Column(Numeric(10, 2), nullable=False, default=Decimal("0.00"))

    rooms = relationship("Room", back_populates="receipt")
    items = relationship("ReceiptItem", back_populates="receipt", cascade="all, delete-orphan")


class Room(Base):
    __tablename__ = "rooms"

    id = Column(String(255), primary_key=True)
    name = Column(String(255), nullable=False)
    creator_id = Column(String(255), ForeignKey("users.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    receipt_id = Column(String(255), ForeignKey("receipts.id", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    is_active = Column(Boolean, nullable=False, default=True)

    creator = relationship("User", back_populates="created_rooms", foreign_keys=[creator_id])
    receipt = relationship("Receipt", back_populates="rooms")
    participants = relationship("RoomParticipant", back_populates="room", cascade="all, delete-orphan")


class RoomParticipant(Base):
    __tablename__ = "room_participants"

    room_id = Column(String(255), ForeignKey("rooms.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    user_id = Column(String(255), ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    joined_at = Column(DateTime, default=datetime.utcnow)

    room = relationship("Room", back_populates="participants")
    user = relationship("User", back_populates="room_participations")


class ReceiptItem(Base):
    __tablename__ = "receipt_items"

    id = Column(String(255), primary_key=True)
    receipt_id = Column(String(255), ForeignKey("receipts.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    name = Column(String(255), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Numeric(10, 3), nullable=False, default=Decimal("1.000"))

    receipt = relationship("Receipt", back_populates="items")
    assignments = relationship("ItemAssignment", back_populates="item", cascade="all, delete-orphan")


class ItemAssignment(Base):
    __tablename__ = "item_assignments"

    item_id = Column(String(255), ForeignKey("receipt_items.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    user_id = Column(String(255), ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)

    item = relationship("ReceiptItem", back_populates="assignments")
    user = relationship("User", back_populates="item_assignments")
