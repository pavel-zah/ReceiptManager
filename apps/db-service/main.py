from fastapi import FastAPI

from routers import items, receipts, rooms, users

app = FastAPI(title="DB Service", version="1.0.0")

app.include_router(users.router)
app.include_router(receipts.router)
app.include_router(rooms.router)
app.include_router(items.router)


@app.get("/health")
def health():
    return {"status": "ok"}
