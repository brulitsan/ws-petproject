# install requirements
FROM python:3.11


WORKDIR /app

COPY . /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install poetry==1.7.1

COPY ./poetry.lock /app/poetry.lock
COPY ./pyproject.toml /app/pyproject.toml

EXPOSE 8000


CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


