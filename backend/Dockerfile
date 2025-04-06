FROM python:3.12-slim
LABEL org.opencontainers.image.source=https://github.com/Stephen-Hallett/ShoppingList
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/


WORKDIR /backend

COPY . /backend

RUN uv sync --frozen

EXPOSE 8000

ENTRYPOINT ["uv", "run", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
