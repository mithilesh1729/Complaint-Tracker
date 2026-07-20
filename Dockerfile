FROM python:3.12-slim

WORKDIR /app

# Install dependencies needed for some Python packages (e.g., psycopg2)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Collect static files (needs dummy env vars if required by settings)
ENV DJANGO_SETTINGS_MODULE=complaint_tracker.settings.prod
ENV SECRET_KEY=dummy-for-build
ENV DB_NAME=dummy DB_USER=dummy DB_PASSWORD=dummy DB_HOST=dummy DB_PORT=5432 FRONTEND_URL=dummy ALLOWED_HOSTS=*
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# Make entrypoint executable
RUN chmod +x scripts/entrypoint.sh

CMD ["scripts/entrypoint.sh"]
