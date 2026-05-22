FROM python:3.12-slim
WORKDIR /app
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY backend ./backend
WORKDIR /app/backend
CMD ["sh","-c","python - <<'PY'\nimport time\nfrom sqlalchemy import create_engine,text\nfrom app.core.config import DATABASE_URL\nfor _ in range(30):\n  try:\n    e=create_engine(DATABASE_URL);\n    with e.connect() as c:c.execute(text('select 1'));\n    break\n  except Exception: time.sleep(2)\nPY\nalembic upgrade head && python seed.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
