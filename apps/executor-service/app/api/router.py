from fastapi import APIRouter, Request
from app.api.schemas import ChatRequest
from app.api.dependencies import DB, LLM, Agent, ReceiptAgent, Graph
from langchain_core.runnables import RunnableConfig
from app.agent.schemas import AgentRoomState
from app.core.logger import get_logger


logger = get_logger(__name__)



router = APIRouter(prefix="/receipt", tags=["receipt agent commands"])


@router.post("/chat")
async def chat_with_agent(
        request: ChatRequest,
        db: DB,
        # llm: LLM,
        agent: ReceiptAgent,
        ) -> dict:
    # TODO: Добавить обработку состояний - отправка на фронт сообщений
    config = RunnableConfig(
        configurable = {
            "user_id": request.user_id,
            "receipt_id": request.receipt_id,
            "db_client": db,
            # "llm": llm,
            "agent": agent,
            "thread_id": f"{request.user_id}:{request.receipt_id}"
        }
    )

    response = await agent.ainvoke(
        request.user_message,
        config=config
    )
    logger.info(response)
    answer = response.get("answer", {})


    return {
        "answer": answer,
        "action_required": response.get("receipt_updated") if response.get("receipt_updated") else "None"
    }
