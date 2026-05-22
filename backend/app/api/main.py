from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Campaign Chronicler API")
app.include_router(router)
