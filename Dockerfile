FROM python:3.8

ENV POETRY_HOME /app
ENV POETRY_VERSION 1.7.1

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade poetry==$POETRY_VERSION

COPY . .

RUN poetry config virtualenvs.create false
RUN poetry install

CMD ["python", "/app/manage.py", "runserver", "0.0.0.0:8000"]
