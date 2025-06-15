FROM python:3.12-slim

WORKDIR /code
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app app
COPY .env.example .env
EXPOSE 8000
CMD ["uvicorn", "app.main:asgi_app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
