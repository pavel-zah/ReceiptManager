from langchain_core.runnables import RunnableConfig
from app.agent.schemas import AgentRoomState, ReceiptItemOutSchema, ReceiptItemBatchOutSchema
from app.core.logger import get_logger
import httpx

logger = get_logger(__name__)


async def getReceiptItems(state: AgentRoomState, config: RunnableConfig) -> dict[str, list | str | ReceiptItemBatchOutSchema] | str:
    """
    Получение всех позиций в чеке.
    Args:
        state: состояние графа
        config: конфиг графа
    Returns:
        Словарь с полем items - список добавленных позиций в виде словарей,
        либо строка с сообщением об ошибке/отсутствии данных и командой для выполнения.
    """

    configurable = config.get("configurable", {})
    metadata = config.get("metadata", {})

    db_client = configurable.get("db_client")
    receipt_id = metadata.get("receipt_id")

    if not db_client:
        logger.error("Error: unable to connect to DB: db_client not found in config configurable.")
        return {"current_command": "SHOW_CHECK",
                "error": "Системная ошибка: нет подключения к БД. Сообщи пользователю об ошибке."
                }

    if not receipt_id:
        logger.error("Error: unable to get receipt items: receipt_id not found in config metadata.")
        return {"current_command": "SHOW_CHECK",
                "error": "Ошибка: отсутствует ID чека. Убедись, что чек был создан до обращения к нему."
                }

    try:

        response = await db_client.get_receipt_items(receipt_id)
        print("*" * 100)
        print(response)
        print("*" * 100)

    except httpx.HTTPStatusError as e:

        status_code = e.response.status_code if e.response else "Unknown"
        error_details = e.response.text if e.response else str(e)
        logger.error(f"HTTP {status_code}: failed to get items for receipt {receipt_id}", exc_info=True)

        return {"current_command": "SHOW_CHECK",
                "error": f"""
                Ошибка API получении позиций в чеке.
                Код ответа: {status_code}.
                Детали: {error_details}.
                Сообщи пользователю об ошибке."""
                }

    except Exception as e:

        logger.error(f"Unexpected error while adding items to receipt {receipt_id}", exc_info=True)
        return {"current_command": "SHOW_CHECK",
                "error": f"Произошла непредвиденная ошибка при добавлении позиций: {str(e)}."
                }

    if item_count := len(response.items):

        logger.info(f"Operation successful: {item_count} items were fetched from receipt {receipt_id}")

        id_mapping = {}
        items_data = []

        formatted_items = []

        for i, item in enumerate(response.items, start=1):

            # id_mapping[i] = item.id

            item_dict = item.model_dump()
            item_dict["id"] = i
            formatted_items.append(ReceiptItemOutSchema(**item_dict))
            items_data.append(item_dict)

        # config["configurable"]["app_state"]["id_mapping"] = id_mapping

        # return {"receipt_items": items_data}
        target_batch = ReceiptItemBatchOutSchema(items=formatted_items)

        return {
            "current_command": "SHOW_CHECK",
            "receipt_items": target_batch,
            "execution_result": f"Успешно получено {len(formatted_items)} поз."
        }

    logger.info(f"Empty items list for receipt {receipt_id}")

    return {
        "current_command": "SHOW_CHECK",
        "receipt_items": ReceiptItemBatchOutSchema(items=[]),
        "answer": "В чеке пока нет добавленных позиций."
    }
