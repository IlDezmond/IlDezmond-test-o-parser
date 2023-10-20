FROM python:3.11-alpine

WORKDIR /app/bot

COPY requirements.txt requirements.txt

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

COPY . .