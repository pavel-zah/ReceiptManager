from fastapi import APIRouter, Request
from app.api.schemas import ChatRequest
from app.api.dependencies import DB, LLM, Agent, ReceiptAgent, Graph
from langchain_core.runnables import RunnableConfig
from app.agent.schemas import AgentRoomState


router = APIRouter(prefix="/receipt", tags=["receipt agent commands"])


@router.post("/chat")
async def chat_with_agent(
        request: ChatRequest,
        db: DB,
        # llm: LLM,
        agent: ReceiptAgent,
        ) -> dict:
    # Создаем объект состояния, который будем отслеживать
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

    # Запускаем агента
    response = await agent.ainvoke(
        request.user_message,
        config=config
    )
    print(response)
    answer = response.get("answer", {})


    # Формируем ответ для фронтенда
    return {
        "answer": answer,
        "action_required": response.get("receipt_updated") if response.get("receipt_updated") else "None, ничо не передало"
    }


#
# @router.post("/chat")
# async def chat_with_agent(
#         request: ChatRequest,
#         db: DB,
#         llm: LLM,
#         agent: Agent,
#         graph: Graph
#         ):
#     # Создаем объект состояния, который будем отслеживать
#     # TODO: Добавить обработку состояний - отправка на фронт сообщений
#     config = RunnableConfig(
#         configurable = {
#             "db_client": db,
#             "llm": llm,
#             "agent": agent,
#             "thread_id": f"{request.user_id}:{request.receipt_id}"},
#         metadata = {
#             "user_id": request.user_id,
#             "receipt_id": request.receipt_id
#         }
#     )
#
#     # Запускаем агента
#     response = await graph.ainvoke(
#         { "messages": [request.user_message] },
#         config=config
#     )
#     print(response)
#
#     # Формируем ответ для фронтенда
#     return {
#         "answer": response.get("answer", "None"),
#         "action_required": "update_receipt" if response.get("receipt_updated") else "None, ничо не передало"
#     }