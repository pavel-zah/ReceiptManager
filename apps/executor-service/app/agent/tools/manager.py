from typing import Callable
from functools import lru_cache
from app.agent.tools.receipt_config_tools import (add_items,
                                                  get_receipt_items,
                                                  get_item,
                                                  update_item,
                                                  delete_item,
                                                  update_receipt,
                                                  get_receipt_info
                                                  )


_all_tools: list[Callable] | None = None
_receipt_tools: list[Callable] | None = None

@lru_cache(maxsize=1)
def build_tools_list() -> list:
    """Создаёт список из callable tools (singleton)"""
    return [add_items,]

@lru_cache(maxsize=1)
def build_receipt_tools_list() -> list:
    """Создаёт список из callable receipt tools (singleton)"""
    return [add_items, get_receipt_items, get_item, update_item, delete_item, update_receipt, get_receipt_info]



def get_all_tools() -> list:
    """
    Возвращает singleton инстанс список tools для агента

    Returns:
        Готовый к использованию список tools
    """
    global _all_tools

    if _all_tools is None:
        _all_tools = build_tools_list()

    return _all_tools



def get_receipt_tools() -> list:
    """
    Возвращает singleton инстанс список receipt tools для агента

    Returns:
        Готовый к использованию список receipt tools
    """
    global _receipt_tools

    if _receipt_tools is None:
        _receipt_tools = build_receipt_tools_list()

    return _receipt_tools


