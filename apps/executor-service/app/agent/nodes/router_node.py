from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from app.agent.schemas import AgentRoomState


async def router(state: AgentRoomState, config: RunnableConfig):
    """Узел-роутер: классифицирует команду"""

    llm = config.get("configurable", {}).get("llm")
    if llm is None:
        return {"error": "no model provided"}

    prompt = ChatPromptTemplate.from_messages([
        ("system", """Ты классификатор команд для редактора чеков.

Доступные команды:
- ADD_ITEMS: добавить позиции или позицию в чек
- REMOVE_ITEM: удалить позиции из чека
- CHANGE_ITEM: изменить параметры существующей позиции
- CHANGE_RECEIPT INFO: применить скидку, изменить количество чаевых,
 изменить дату оплаты, изменить место оплаты или добавить сервисный сбор
- SHOW_CHECK: показать чек или вывести позиции из чека
- UNKNOWN: неизвестная команда

Верни ТОЛЬКО название команды, без объяснений."""),
        ("user", "{input}")
    ])

    chain = prompt | llm
    response = await chain.ainvoke({"input": state["messages"][-1]})
    print("=" * 50)
    print(response)
    print("=" * 50)

    return {"command": response.content.strip(),
            "error": None}