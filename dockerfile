FROM python:3.12-alpine
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apk add --no-cache curl build-base

WORKDIR /app

COPY pyproject.toml .
COPY requirements.txt .
COPY src/ ./src/
COPY main.py .

RUN uv pip install -r requirements.txt --system

EXPOSE 8000

CMD ["uv", "run", "main.py"]
