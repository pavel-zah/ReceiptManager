from app.core.config import get_settings
from app.core.logger import get_logger
from langchain.tools import tool
from langchain_core.runnables import RunnableConfig
from app.agent.schemas import ReceiptItemBatchCreateSchema, ReceiptItemUpdateSchema, ReceiptItemOutSchema, AgentRoomState
from app.schemas.receipt_item import ReceiptItemUpdate
import httpx

logger = get_logger(__name__)


async def add_items(state: AgentRoomState, config: RunnableConfig) -> dict[str, list | str | bool]:
    """
    Добавление позиций чека в базу данных.
    Args:
        receipt_items_object: список позиций для добавления в чек
    Returns:
        Словарь с полем items - список добавленных позиций в виде словарей,
        либо строка с сообщением об ошибке/отсутствии данных и командой для выполнения.
    """

    receipt_items_object = state.get("items_to_add")
    if receipt_items_object is None:
        return {"error": "Add items: no items were provided"}

    configurable = config.get("configurable", {})
    metadata = config.get("metadata", {})

    db_client = configurable.get("db_client")
    receipt_id = metadata.get("receipt_id")

    if not db_client:
        logger.error("Error: unable to connect to DB: db_client not found in config configurable.")
        return {"error": "Системная ошибка: нет подключения к БД. Сообщи пользователю об ошибке."}

    if not receipt_id:
        logger.error("Error: unable add items: receipt_id not found in config metadata.")
        return {"error": "Ошибка: отсутствует ID чека. Убедись, что чек был создан до добавления позиций."}

    try:

        payload_for_db = [item.to_db_model() for item in receipt_items_object.items] # float to Decimal

        response = await db_client.add_items(receipt_id=receipt_id, payload=payload_for_db)

    except httpx.HTTPStatusError as e:

        status_code = e.response.status_code if e.response else "Unknown"
        error_details = e.response.text if e.response else str(e)
        logger.error(f"HTTP {status_code}: failed to add items to receipt {receipt_id}", exc_info=True)

        return {"error": f"""
            Ошибка API при добавлении позиций в чек.
            Код ответа: {status_code}.
            Детали: {error_details}.
            Исправь данные и попробуй снова."""}

    except Exception as e:

        logger.error(f"Unexpected error while adding items to receipt {receipt_id}", exc_info=True)
        return {"error": f"Произошла непредвиденная ошибка при добавлении позиций: {str(e)}."}


    if item_count := len(response.items):

        logger.info(f"Operation successful: {item_count} items were added to receipt with id {receipt_id}")

        return {"added_items": response.model_dump(), "receipt_updated": True, "items_to_add": None, "error": None}

    logger.warning(f"Error: empty payload for receipt {receipt_id}")

    return {"error": "Ошибка. Не было добавлено ни одной позиции. Проверь переданные данные"}

