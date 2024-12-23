FROM python:3.12-slim

COPY . todo

WORKDIR todo

RUN pip install -r requirements.txt

EXPOSE 80

VOLUME /app/data

CMD uvicorn todo.main:app --host 0.0.0.0 --port 80
