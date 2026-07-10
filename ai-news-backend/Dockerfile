FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir apscheduler gunicorn

COPY . .

RUN mkdir -p /data
ENV DATABASE_URL=sqlite:////data/ainews.db
ENV SECRET_KEY=f3a9c7e2-8b4d-4e1a-9f6c-2d5a8e3b7c1e-prod
ENV OPENAI_API_KEY=b126f0b210b344749ce882be1395be05.4Bp6eFxzgZI6xMVs
ENV OPENAI_BASE_URL=https://open.bigmodel.cn/api/paas/v4
ENV OPENAI_MODEL=glm-4-flash
ENV CORS_ORIGINS=*

RUN python seed_deploy.py || true

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
