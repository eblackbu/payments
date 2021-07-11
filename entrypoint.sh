#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done
fi

python manage.py flush --no-input
python manage.py migrate --skip-checks
python manage.py load_trash
python manage.py collectstatic --no-input

exec "$@"