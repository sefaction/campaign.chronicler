FROM python:3.12-slim
WORKDIR /app
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY backend ./backend
WORKDIR /app/backend
CMD ["sh","-c","python - <<'PY'\nimport time\nfrom sqlalchemy import create_engine,text\nfrom app.core.config import DATABASE_URL\nready=False\nfor _ in range(30):\n  try:\n    e=create_engine(DATABASE_URL)\n    with e.connect() as c:\n      c.execute(text('select 1'))\n    ready=True\n    break\n  except Exception:\n    time.sleep(2)\nprint('db_ready=', ready)\nPY\nif alembic upgrade head; then echo 'migrations ok'; else echo 'migrations failed, continuing'; fi\nif python seed.py; then echo 'seed ok'; else echo 'seed failed, continuing'; fi\nuvicorn app.main:app --host 0.0.0.0 --port 8000"]
