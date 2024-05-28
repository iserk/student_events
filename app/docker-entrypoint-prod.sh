#!/bin/bash

# # Verify that Postgres is healthy before applying the migrations and running the Django development server
# if [ "$DATABASE" = "postgres" ]; then echo "Waiting for postgres..."
#     while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
#       sleep 0.1
#     done
#     echo "PostgreSQL is accepting connections"
# fi

echo "Apply database migrations"
python manage.py migrate

echo "Starting server"
/usr/local/bin/gunicorn sams.wsgi:application --workers 2 --bind :8000