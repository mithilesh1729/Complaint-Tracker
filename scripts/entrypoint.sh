#!/bin/bash
set -e

# Wait for Postgres
echo "Waiting for postgres..."
while ! pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"
do
  echo "Waiting for postgres..."
  sleep 2
done

echo "PostgreSQL started"

# Run migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Start Gunicorn
# 2 * CPU cores + 1 is the recommended number of workers
echo "Starting Gunicorn..."
exec gunicorn complaint_tracker.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --threads 2 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
