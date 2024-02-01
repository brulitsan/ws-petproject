FROM python:3.8

ENV POETRY_HOME /app
ENV POETRY_VERSION 1.7.1

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && pip install poetry==1.7.1

COPY . .

CMD ["python", "/manage.py", "runserver", "0.0.0.0:8000"]
