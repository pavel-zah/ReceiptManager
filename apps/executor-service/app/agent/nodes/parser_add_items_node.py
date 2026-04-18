from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from app.agent.schemas import AgentRoomState
from app.agent.tools.receipt_config_tools import addItems
from app.agent.schemas import ReceiptItemBatchCreateSchema


async def parser_add_items(state: AgentRoomState, config: RunnableConfig):
    """Узел графа: парсер блюд из запроса"""


    llm = config.get("configurable", {}).get("llm")
    if llm is None:
        return {"error": "no model provided"}

    llm_with_structured_output = llm.with_structured_output(ReceiptItemBatchCreateSchema)

    prompt = ChatPromptTemplate.from_messages([
        ("system", """Ты помощник, который извлекает информацию о позициях чека из запроса пользователя.

    Извлеки следующие данные для каждой позиции из последнего сообщения пользователя:
    - dish_name: название блюда
    - quantity: количество (по умолчанию 1, если не указано)
    - price: цена в рублях

    Соблюдай правила:
    - Если указана цена, но ты не можешь определить за штуку это или за все,
    то предполагай, что это цена за одну единицу - позицию.
    - Если ты не можешь определить название блюда или его цену, то запиши об этом информацию в поле error.
    - Если ты определил необходимую информацию, то оставь поле error пустым"""),
        ("user", "{input}")
    ])

    try:
        chain = prompt | llm_with_structured_output
        response = await chain.ainvoke({"input": state["messages"][-1:]}) # берем только 1 последних сообщения
        return {"items_to_add": response, "command": "ADD_ITEMS", "error": None}
    except Exception as e:
        return {"error": f"Не удалось распознать данные: {str(e)}"}

    # # Вызываем toolthread_id = config["configurable"]["thread_id"]
    # result = await addItems.ainvoke({'receipt_items_object': response.model_dump()}, config)

    return {"items_to_add": response, "command": "add_dish"}