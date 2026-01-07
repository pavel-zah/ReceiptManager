from dataclasses import dataclass, field
from decimal import Decimal
from typing import List


@dataclass
class ParsedItemDTO:
    """Сырая позиция из чека, найденная OCR"""
    name: str
    price: Decimal
    quantity: Decimal


@dataclass
class ParsedReceiptDTO:
    """Сырой чек, найденный OCR"""
    paid_at: str
    items: List[ParsedItemDTO] = field(default_factory=list)
    tip: Decimal = Decimal("0.00")
    service: Decimal = Decimal("0.00")
