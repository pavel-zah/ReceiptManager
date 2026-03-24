from app.core.config import get_settings
from app.core.logger import get_logger
from langchain.tools import tool
from langchain_core.runnables import RunnableConfig
from app.agent.schemas import ReceiptItem
from typing import List

from app.clients.db_client import DBClient
logger = get_logger(__name__)


@tool
def addItems(items: List[ReceiptItem], config: RunnableConfig) -> str:
    """
    Добавление позиций чека в базу данных.
    Args:
        items: список позиций для добавления в чек
    """
    configurable = config.get("configurable", {})
    metadata = config.get("metadata", {})

    db_client = configurable.get("db_client")
    receipt_id = metadata.get("receipt_id")

    if not db_client:
        logger.error("Error: unable to connect to DB: db_client not found in config configurable.")
        return "Ошибка: соединение с БД недоступно"

    if not receipt_id:
        logger.error("Error: unable add items: receipt_id not found in config metadata.")
        return "Ошибка: соединение с БД недоступно"
    return ""




