FROM python:3.11-slim

WORKDIR /app

COPY . /app/

RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["python", "main.py"]
CMD ["--help"]
