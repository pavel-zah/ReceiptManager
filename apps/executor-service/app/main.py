from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.api.routers import api_router
from app.clients.db_client import DBClient

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.db_client = DBClient()
    yield

def create_app() -> FastAPI:
    app = FastAPI(title="Executor service", version="1.0.0")

    app.include_router(api_router.router)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app

app = create_app()