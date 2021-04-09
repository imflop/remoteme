#!/bin/bash

source /venv/bin/activate
mkdir -p logs

python manage.py migrate --noinput
python manage.py collectstatic --noinput

celery -A remoteme.celery_remoteme:app beat --logfile=/app/logs/celery_beat.log -l INFO &
celery -A remoteme.celery_remoteme:app worker --logfile=/app/logs/celery_worker.log -E -l INFO &

gunicorn remoteme.wsgi:application \
--chdir /app \
--bind 0.0.0.0:8080 \
--workers 5 \
--timeout 300 \
--error-logfile /app/logs/gunicorn_web_error.log