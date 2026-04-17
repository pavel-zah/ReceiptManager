from fastapi import FastAPI
from contextlib import asynccontextmanager
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from fastapi.middleware.cors import CORSMiddleware
from app.api import router
from app.core.config import settings
from app.clients.db_client import DBClient
from app.agent.llm import get_llm
from app.agent.agent import get_agent
from app.agent.graph import get_graph
from app.core.logger import get_logger
import uvicorn
import asyncio
import sys


logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncPostgresSaver.from_conn_string(settings.langgraph_db_url) as checkpointer:
        logger.info("Initialized postgres checkpointer instance")
        await checkpointer.setup()
        logger.info("Postgres checkpointer was set up")
        app.state.llm = get_llm()
        app.state.db_client = DBClient()
        app.state.agent = get_agent()
        app.state.graph = await get_graph(checkpointer)
        yield
        await app.state.db_client.close()


def create_app() -> FastAPI:
    app = FastAPI(title="Executor service", version="1.0.0", lifespan=lifespan)

    #TODO change name, not router.router
    app.include_router(router.router)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # В продакшене лучше указать конкретные домены
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app

app = create_app()

if __name__ == "__main__":

    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    uvicorn.run(app, host="0.0.0.0", port=8002)