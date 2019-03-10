FROM python:3-alpine

WORKDIR /app

COPY *.py /app/

RUN ["pip", "install", "WazeRouteCalculator"]

CMD ["python3", "-m", "main"]
