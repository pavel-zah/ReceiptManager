from fastapi import Request, Depends
from typing import Annotated
from app.clients.db_client import DBClient


def get_db_client(request: Request) -> DBClient:
    """Достаём DBClient из app.state - один инстанс."""
    return request.app.state.db_client

DB = Annotated[DBClient, Depends(get_db_client)]