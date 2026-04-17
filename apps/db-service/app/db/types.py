from sqlalchemy import TypeDecorator, String
from app.db.enums import ReceiptStatusEnum, RoomStatusEnum, PaidStatusEnum


class EnumAsString(TypeDecorator):
    """Автоматически конвертирует Enum.value при записи и Enum при чтении"""
    impl = String
    cache_ok = True

    def __init__(self, enum_class, length: int = 20):
        self.enum_class = enum_class
        self.length = length
        super().__init__(length=length)

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, self.enum_class):
            return value.value
        if isinstance(value, str):
            return value
        raise TypeError(f"Expected {self.enum_class.__name__} or str, got {type(value)}")

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return self.enum_class(value)