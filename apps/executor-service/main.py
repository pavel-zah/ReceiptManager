from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api import router
from app.clients.db_client import DBClient
from app.agent.agent import get_agent
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db_client = DBClient()
    app.state.agent = get_agent()
    yield
    await app.state.db_client.close()


def create_app() -> FastAPI:
    app = FastAPI(title="Executor service", version="1.0.0", lifespan=lifespan)

    #TODO change name, not router.router
    app.include_router(router.router)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8002)