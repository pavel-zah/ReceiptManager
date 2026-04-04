from app.core.config import get_settings
from app.core.logger import get_logger
from langchain.tools import tool
from langchain_core.runnables import RunnableConfig
from app.agent.schemas import ReceiptItemBatchCreateSchema, ReceiptItemUpdateSchema, ReceiptItemOutSchema
from app.schemas.receipt_item import ReceiptItemUpdate
import httpx

logger = get_logger(__name__)


@tool
async def addItems(receipt_items_object: ReceiptItemBatchCreateSchema, config: RunnableConfig) -> dict[str, list | str] | str:
    """
    Добавление позиций чека в базу данных.
    Args:
        receipt_items_object: список позиций для добавления в чек
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
        return "Системная ошибка: нет подключения к БД. Сообщи пользователю об ошибке."

    if not receipt_id:
        logger.error("Error: unable add items: receipt_id not found in config metadata.")
        return "Ошибка: отсутствует ID чека. Убедись, что чек был создан до добавления позиций."

    try:

        payload_for_db = [item.to_db_model() for item in receipt_items_object.items] # float to Decimal

        response = await db_client.add_items(receipt_id=receipt_id, payload=payload_for_db)

    except httpx.HTTPStatusError as e:

        status_code = e.response.status_code if e.response else "Unknown"
        error_details = e.response.text if e.response else str(e)
        logger.error(f"HTTP {status_code}: failed to add items to receipt {receipt_id}", exc_info=True)

        return f"""
            Ошибка API при добавлении позиций в чек.
            Код ответа: {status_code}.
            Детали: {error_details}.
            Исправь данные и попробуй снова."""

    except Exception as e:

        logger.error(f"Unexpected error while adding items to receipt {receipt_id}", exc_info=True)
        return f"Произошла непредвиденная ошибка при добавлении позиций: {str(e)}."


    if item_count := len(response.items):

        if "app_state" not in configurable:
            configurable["app_state"] = {}

        configurable["app_state"]["receipt_updated"] = True

        logger.info(f"Operation successful: {item_count} items were added to receipt with id {receipt_id}")

        return response.model_dump()

    logger.warning(f"Error: empty payload for receipt {receipt_id}")

    return "Ошибка. Не было добавлено ни одной позиции. Проверь переданные данные"


@tool
async def getReceiptItems(config: RunnableConfig) -> dict[str, list | str] | str:
    """
    Получение всех позиций в чеке.
    Args:
        None
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
        return "Системная ошибка: нет подключения к БД. Сообщи пользователю об ошибке."

    if not receipt_id:
        logger.error("Error: unable to get receipt items: receipt_id not found in config metadata.")
        return "Ошибка: отсутствует ID чека. Убедись, что чек был создан до обращения к нему."

    try:

        response = await db_client.get_receipt_items(receipt_id)

    except httpx.HTTPStatusError as e:

        status_code = e.response.status_code if e.response else "Unknown"
        error_details = e.response.text if e.response else str(e)
        logger.error(f"HTTP {status_code}: failed to get items for receipt {receipt_id}", exc_info=True)

        return f"""
            Ошибка API получении позиций в чеке.
            Код ответа: {status_code}.
            Детали: {error_details}.
            Сообщи пользователю об ошибке."""

    except Exception as e:

        logger.error(f"Unexpected error while adding items to receipt {receipt_id}", exc_info=True)
        return f"Произошла непредвиденная ошибка при добавлении позиций: {str(e)}."

    if item_count := len(response.items):

        logger.info(f"Operation successful: {item_count} items were fetched from receipt {receipt_id}")

        id_mapping = {}
        items_data = []

        for i, item in enumerate(response.items, start=1):

            id_mapping[i] = item.id

            item_dict = item.model_dump()
            item_dict["id"] = i
            items_data.append(item_dict)

        config["configurable"]["app_state"]["id_mapping"] = id_mapping

        return {"items": items_data}

    logger.info(f"Empty items list for receipt {receipt_id}")

    return "В чеке отсутствуют позиции"


@tool
async def get_item(item_display_id: int, config: RunnableConfig) -> dict[str, int | str | float] | str:
    """
    Получение информации о позиции по ее id.
    Args:
        item_display_id: id позиции в чеке, положительное целое число. Используй ID,
         который был получен из последнего вызова getReceiptItems
    Returns:
        Словарь с информацией о позиции,
        либо строка с сообщением об ошибке/отсутствии данных и командой для выполнения.
    """
    configurable = config.get("configurable", {})

    app_state = configurable.get("app_state", {})

    db_client = configurable.get("db_client")
    if not db_client:
        logger.error("Error: unable to connect to DB: db_client not found in config configurable.")
        return "Системная ошибка: нет подключения к БД. Сообщи пользователю об ошибке."

    id_mapping = app_state.get("id_mapping")
    if not id_mapping:
        return "Ошибка по получении позиции по ее id, сначала получи список всех позиций в чеке"

    item_real_id = id_mapping.get(item_display_id)
    if not item_real_id:
        return ("Ошибка по получении позиции по ее id,"
                " попробуй получить список всех позиций в чеке и повторить попытку на основе новых данных")

    try:
        response = await db_client.get_item(item_real_id)

    except httpx.HTTPStatusError as e:

        status_code = e.response.status_code if e.response else "Unknown"
        error_details = e.response.text if e.response else str(e)
        logger.error(f"HTTP {status_code}: failed to get item by id {item_real_id}", exc_info=True)

        return f"""
            Ошибка API получении позиции.
            Код ответа: {status_code}.
            Детали: {error_details}.
            Сообщи пользователю об ошибке."""

    except Exception as e:

        logger.error("Unexpected error while getting item by id %s", item_real_id, exc_info=True)
        return f"Произошла непредвиденная ошибка при получении позиции: {str(e)}."

    if response:

        logger.info("Operation successful: item with id %s was fetched", item_real_id)

        response_dict = response.model_dump()
        response_dict["id"] = item_display_id
        return response_dict

    return f"Элемент с таким id не был найден, проверь корректность введенных данных"


#TODO lazy formating in logger


@tool
async def update_item(
        item_display_id,
        item_info: ReceiptItemUpdateSchema,
        config: RunnableConfig
) -> dict[str, int | str | float] | str:
    """
    Обновление информации о позиции по ее id.
    Args:
        item_display_id: id позиции в чеке, положительное целое число. Используй ID,
         который был получен из последнего вызова getReceiptItems
        item_info: объект с полями для обновления.
    Returns:
        Словарь с информацией об обновленной позиции,
        либо строка с сообщением об ошибке/отсутствии данных и командой для выполнения.
    """
    configurable = config.get("configurable", {})

    app_state = configurable.get("app_state", {})

    db_client = configurable.get("db_client")
    if not db_client:
        logger.error("Error: unable to connect to DB: db_client not found in config configurable.")
        return "Системная ошибка: нет подключения к БД. Сообщи пользователю об ошибке."

    id_mapping = app_state.get("id_mapping")
    if not id_mapping:
        return "Ошибка по обновлении позиции, сначала получи список всех позиций в чеке"

    item_real_id = id_mapping.get(item_display_id)
    if not item_real_id:
        return ("Ошибка по обновлении позиции,"
                " попробуй получить список всех позиций в чеке и повторить попытку на основе новых данных")

    try:
        response = await db_client.update_item(item_real_id, item_info.to_db_update())

    except httpx.HTTPStatusError as e:

        status_code = e.response.status_code if e.response else "Unknown"
        error_details = e.response.text if e.response else str(e)
        logger.error(f"HTTP {status_code}: failed to update item {item_real_id}", exc_info=True)

        return f"""
            Ошибка API обновлении позиции.
            Код ответа: {status_code}.
            Детали: {error_details}.
            Сообщи пользователю об ошибке."""

    except Exception as e:

        logger.error("Unexpected error while updating item by id %s", item_real_id, exc_info=True)
        return f"Произошла непредвиденная ошибка при обновлении позиции: {str(e)}."


    return ReceiptItemOutSchema.model_validate({
        **response.model_dump(),
        "id": item_display_id
    }).model_dump()

# @tool
# async def delete_item(???, config: RunnableConfig) -> str:
#     ...



# @tool
# async def update_receipt_info(config: RunnableConfig):

# print(addItems.args_schema.schema())