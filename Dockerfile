# install requirements
FROM python:3.11 as builder

WORKDIR /app

RUN pip install poetry==1.7.1
RUN apt-get update && apt-get install -y netcat-openbsd

COPY poetry.lock /app/poetry.lock
COPY pyproject.toml /app/pyproject.toml

# Only application
FROM builder as slim

COPY . /app/

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi
