from fastapi import APIRouter, Request
from app.api.schemas import ChatRequest
from app.api.dependencies import DB, Agent
from langchain_core.runnables import RunnableConfig



router = APIRouter(prefix="/receipt", tags=["receipt agent commands"])


@router.post("/chat")
async def chat_with_agent(
        request: ChatRequest,
        db: DB,
        agent: Agent
        ):
    # Создаем объект состояния, который будем отслеживать
    # TODO: Добавить обработку состояний - отправка на фронт сообщений
    config = RunnableConfig(
        configurable = {"db_client": db, "receipt_updated": False},
        metadata = {"receipt_id": request.receipt_id}
    )

    # Запускаем агента
    response = await agent.ainvoke(
        message=request.user_message,
        session_id=1,
        config=config
    )

    # Формируем ответ для фронтенда
    return {
        "answer": response["answer"],
        "tools_used": response["tools_used"],
        "action_required": "update_receipt" if config.get("app_state", {}).get("receipt_updated") else None
    }