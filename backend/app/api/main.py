from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Campaign Chronicler API")
app.include_router(router)

@app.get("/")
def root():
    return {
        "name": "Campaign Chronicler API",
        "status": "ok",
        "health": "/health",
        "docs": "/docs",
        "openapi": "/openapi.json"
    }

@app.get("/health")
def health():
    return {"status": "ok"}
