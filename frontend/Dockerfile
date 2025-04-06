FROM python:3.12-slim
LABEL org.opencontainers.image.source=https://github.com/Stephen-Hallett/ShoppingList
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /frontend

COPY . /frontend

RUN uv sync --frozen

EXPOSE 6969

ENTRYPOINT [ "uv", "run", "streamlit", "run", "app.py", "--server.port", "6969"]
