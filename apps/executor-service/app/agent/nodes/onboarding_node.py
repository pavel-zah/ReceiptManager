from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from app.agent.schemas import AgentRoomState


async def onboarding_node(state: AgentRoomState, config: RunnableConfig):
    """Узел-приветствие: кратко отвечает на вопрос и напоминает об основном функционале"""

    llm = config.get("configurable", {}).get("llm")
    if llm is None:
        return {"error": "no model provided"}

    prompt = ChatPromptTemplate.from_messages([
        ("system", """Ты помощник по управлению для редактора чеков.
        Твоя задача кратко ответить на запрос пользователя и напомнить ему о том, зачем нужна данная система.
        Отвечать необходимо от первого лица - как будто ты и есть вся система и это ты умеешь выполнять все действия.
        Ты умеешь:
    - добавлять блюдо в чек
    - получать список всех блюд в чеке
    - изменять информацию блюда (название, цена, количество)
    - удалять блюдо из чека
    - изменять информацию о чеке, такую как: название места, чаевые, сервисный сбор, дату

    Ты можешь немного отходить от сценария в зависимости от запроса пользователя,
    но помни, что твоя основная задача это ответ краткий ответ на запрос пользователя."""),
        ("user", "{input}")
    ])

    chain = prompt | llm
    response = await chain.ainvoke({"input": state["messages"][-1]})

    return {"command": response.content.strip()}