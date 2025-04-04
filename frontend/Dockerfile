FROM python:3.12-slim
LABEL org.opencontainers.image.source=https://github.com/Stephen-Hallett/ShoppingList

WORKDIR /frontend

COPY . /frontend

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 6969

ENTRYPOINT [ "streamlit", "run", "app.py", "--server.port", "6969"]
