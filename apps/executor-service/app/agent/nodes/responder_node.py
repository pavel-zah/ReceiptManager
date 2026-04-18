from langchain_core.runnables import RunnableConfig
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from app.agent.schemas import AgentRoomState


async def responder(state: AgentRoomState, config: RunnableConfig):
    llm = config.get("configurable", {}).get("llm")
    if llm is None:
        return {"error": "no model provided"}

    command = state.get("current_command")
    execution_result = state.get("execution_result")
    receipt_items = state.get("receipt_items")

    receipt_items_str = None
    if receipt_items:
        if hasattr(receipt_items, 'model_dump'):
            receipt_items_str = str(receipt_items.model_dump())
        elif isinstance(receipt_items, dict):
            receipt_items_str = str(receipt_items)
        else:
            receipt_items_str = str(receipt_items)

    added_items = state.get('added_items')
    added_items_str = None
    if added_items:
        if isinstance(added_items, dict):
            added_items_str = str(added_items)
        elif hasattr(added_items, 'model_dump'):
            added_items_str = str(added_items.model_dump())
        else:
            added_items_str = str(added_items)

    params = state.get('params')
    params_str = None
    if params:
        if isinstance(params, dict):
            params_str = str(params)
        elif hasattr(params, 'model_dump'):
            params_str = str(params.model_dump())
        else:
            params_str = str(params)

    prompts_map = {
        "ADD_ITEMS": (
            "Подтверди добавление позиций в чек. "
            f"Добавленные данные: {added_items_str}. "
            "Перечисли названия и количество."
        ),
        "REMOVE_ITEM": (
            "Подтверди удаление позиции. "
            f"Результат: {execution_result}. "
            "Напиши, что позиция успешно убрана из чека."
        ),
        "CHANGE_ITEM": (
            "Подтверди изменение позиции. "
            f"Новые параметры: {params_str}. "
            "Сообщи, что мы обновили информацию."
        ),
        "APPLY_DISCOUNT": (
            "Подтверди применение скидки. "
            f"Детали: {params_str}. "
            "Напиши итоговую выгоду или новый статус чека."
        ),
        "SHOW_CHECK": (
            "Пользователь хочет увидеть чек. "
            f"Результат вызова метода: {execution_result}"
            f"Данные чека: {receipt_items_str}. "
            "Выведи чек в удобном текстовом виде."
        )
    }

    specific_instruction = prompts_map.get(
        command,
        f"Просто подтверди выполнение операции: {command}. Результат: {execution_result}"
    )

    full_prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "Ты — помощник по управлению ресторанными чеками. Твоя задача — вежливо "
            "и кратко ответить пользователю на основе выполненной операции.\n"
            f"ИНСТРУКЦИЯ: {specific_instruction}"
        )),
        ("placeholder", "{history}")
    ])

    try:
        messages = state.get("messages", [])
        history = []
        if messages:
            last_message = messages[-1]
            if isinstance(last_message, str):
                history = [HumanMessage(content=last_message)]
            else:
                history = [last_message]

        chain = full_prompt | llm
        response = await chain.ainvoke({
            "history": history
        })

        return {
            "messages": [response],
            "answer": [response],
            "current_command": None,
            "execution_result": None,
            "added_items": None,
            "params": None,
            "error": None
        }
    except Exception as e:
        return {"error": f"Ошибка формирования ответа: {str(e)}"}