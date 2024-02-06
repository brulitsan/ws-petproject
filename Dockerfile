# install requirements
FROM python:3.11


WORKDIR /app

COPY . /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


RUN pip install poetry==1.7.1

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

RUN pip install celery==5.3.5

EXPOSE 8000

