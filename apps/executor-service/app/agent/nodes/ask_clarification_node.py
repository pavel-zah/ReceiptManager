from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from app.agent.schemas import AgentRoomState


async def ask_clarification(state: AgentRoomState, config: RunnableConfig):
    """Узел графа: формирует вопрос к пользователю, если данных недостаточно"""

    llm = config.get("configurable", {}).get("llm")
    if llm is None:
        return {"error": "no model provided"}

    error = state.get("error")
    last_user_messages =  ". ".join([msg.content if hasattr(msg, 'content') else str(msg)
    for msg in state.get("messages", [])[-3:]])
    current_command = state.get("current_command", "UNKNOWN")

    prompt = ""

    if current_command == "ADD_ITEMS":
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Пользователь хотел добавить блюдо, но мы не поняли: {error}.
        Последние сообщения пользователя: "{last_user_messages}"
        
        Сформулируй короткий уточняющий вопрос. 
        Например: "Какое именно блюдо вы хотите добавить?" или "Уточните, пожалуйста, количество".""")
        ])
    if current_command == "UNKNOWN":
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Пользователь задал вопрос, но мы не поняли: {error}.
               Последние сообщения пользователя: "{last_user_messages}"

               Сформулируй короткий уточняющий вопрос. 
               Например: "Какое именно блюдо вы хотите добавить?" """)
        ])

    chain = prompt | llm
    response = await chain.ainvoke({"error": error, "last_user_messages":last_user_messages})

    return {
        "messages": [response],
        "answer": [response],
        "error": None
    }