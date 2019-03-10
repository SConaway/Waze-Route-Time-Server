FROM python:3-alpine

WORKDIR /app

COPY * /app/

RUN ["pip", "install", "-r", "requirements.txt"]

CMD ["python3", "-m", "main"]
