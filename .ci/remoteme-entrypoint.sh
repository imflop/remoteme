#!/bin/bash

while ! curl http://postgres:5432/ 2>&1 | grep '52'; do sleep 1; done

source venv/bin/activate
mkdir -p logs

python manage.py migrate --noinput
python manage.py collectstatic --noinput

gunicorn remoteme.wsgi:application \
--chdir /app \
--bind 0.0.0.0:8080 \
--workers 5 \
--timeout 300 \
--error-logfile /app/logs/gunicorn_web_error.log