from fastapi import Request, Depends
from typing import Annotated
from app.clients.db_client import DBClient
from app.agent.agent import AgentExecutor
from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph.state import CompiledStateGraph


def get_db_client(request: Request) -> DBClient:
    """получение DBClient из app.state."""
    return request.app.state.db_client

DB = Annotated[DBClient, Depends(get_db_client)]


def get_current_agent(request: Request):
    return request.app.state.agent

Agent = Annotated[AgentExecutor, Depends(get_current_agent)]

def get_current_graph(request: Request):
    return request.app.state.graph

Graph = Annotated[CompiledStateGraph, Depends(get_current_graph)]

def get_current_llm(request: Request):
    return request.app.state.llm

LLM = Annotated[BaseChatModel, Depends(get_current_llm)]
