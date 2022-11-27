FROM python:3.11-alpine

WORKDIR /app

RUN pip install twitter

ENTRYPOINT [ "/app/main.py" ]
