from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from app.agent.schemas import AgentRoomState
from app.agent.tools.receipt_config_tools import addItems
from app.agent.schemas import ReceiptItemBatchCreateSchema


def unknow_command_node(state: AgentRoomState, config: RunnableConfig):
    """Неизвестная команда"""

    return {"error": "ошибка", "answer": "unexpected error", "tools_used": None}