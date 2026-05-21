import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@postgres:5432/campaign_chronicler")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
