FROM python:3.12-slim

WORKDIR /app
COPY api/ /app/api/
COPY data/ /app/data/

RUN pip install --no-cache-dir fastapi uvicorn pydantic

EXPOSE 8000
CMD ["uvicorn", "app:app", "--app-dir", "api", "--host", "0.0.0.0", "--port", "8000"]
