FROM python:3.11

WORKDIR /app

COPY . /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && pip install poetry==1.7.1

COPY ./pyproject.toml /app/pyproject.toml
COPY ./poetry.lock /app/poetry.lock

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


