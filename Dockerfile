# Base Image
FROM python:3.12-slim

# Working Directory
WORKDIR /app

# Copy dependency file first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Copy project
# This copies your entire project into /app.
COPY . .

EXPOSE 8000

# Start Django for development
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
