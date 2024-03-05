#!/bin/sh
echo "Waiting for postgres..."
while ! nc -z database "${POSTGRES_PORT}"; do
  sleep 1
done
echo "PostgreSQL started"

# shellcheck disable=SC2164
poetry run python main/manage.py runserver "${ROOT_URL}"

exec "$@"
