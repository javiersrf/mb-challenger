FROM python:3.12-alpine AS builder

RUN apk add --no-cache curl build-base

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml .
COPY requirements.txt .
COPY src/ ./src/
COPY main.py .

RUN uv pip install -r requirements.txt --system --target=/app/.packages

FROM python:3.12-alpine

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY --from=builder /app/.packages /usr/local/lib/python3.12/site-packages

COPY src/ ./src/
COPY main.py .

EXPOSE 8000

CMD ["uv", "run", "main.py"]
