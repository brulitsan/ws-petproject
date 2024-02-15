#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z database ${POSTGRES_PORT}; do
  sleep 1
done

echo "PostgreSQL started"

cd main
poetry run python manage.py runserver ${ROOT_URL}

exec "$@"
