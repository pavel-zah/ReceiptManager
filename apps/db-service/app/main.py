from fastapi import FastAPI
from app.api.routers import items, receipts, rooms, users
from contextlib import asynccontextmanager

app = FastAPI(title="DB Service", version="1.0.0")

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     app.state.db_client = DBClient()
#     yield

def create_app() -> FastAPI:
    app = FastAPI(title="DB API", version="1.0.0")

    app.include_router(users.router)
    app.include_router(receipts.router)
    app.include_router(rooms.router)
    app.include_router(items.router)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app

app = create_app()