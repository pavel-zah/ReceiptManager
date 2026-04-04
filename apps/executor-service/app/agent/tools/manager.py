from typing import Callable
from functools import lru_cache
from app.agent.tools.receipt_config_tools import addItems


_all_tools: list[Callable] | None = None

@lru_cache(maxsize=1)
def build_tools_list_agent() -> list:
    """Создаёт список из callable tools (singleton)"""
    return [addItems,]


def get_all_tools() -> list:
    """
    Возвращает singleton инстанс список tools для агента

    Returns:
        Готовый к использованию список tools
    """
    global _all_tools

    if _all_tools is None:
        _all_tools = build_tools_list_agent()

    return _all_tools