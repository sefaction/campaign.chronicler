import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router

app = FastAPI(title="Campaign Chronicler API")

cors_origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:15173,http://127.0.0.1:15173,http://192.168.1.2:15173",
)
origins = [o.strip() for o in cors_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
