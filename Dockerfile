FROM python:3-alpine

WORKDIR /app

RUN ["pip", "install", "WazeRouteCalculator ", "pyyaml"]

COPY *.py /app/

CMD ["python3", "-m", "main"]
