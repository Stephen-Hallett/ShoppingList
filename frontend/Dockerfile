FROM python:3.12-slim

WORKDIR /frontend

COPY . /frontend

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 6969

ENTRYPOINT [ "streamlit", "run", "app.py", "--server.port", "6969"]
