FROM python:3.11

WORKDIR /app/backend

COPY requirements.txt requirements.txt

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

COPY . .
COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh