FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
# Added libpq-dev for PostgreSQL, and cairo/pango for PDF generation features (xhtml2pdf)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    python3-dev \
    libmariadb-dev-compat \
    libmariadb-dev \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    libffi-dev \
    libcairo2-dev \
    libpango1.0-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/logs /app/staticfiles /app/media

# Provide dummy key for collectstatic to run without failing
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=config.ecommerce.settings \
    SECRET_KEY=dummy-key-for-collectstatic

# Collect static files during the docker build
RUN python manage.py collectstatic --no-input

# Set default port and expose it
ENV PORT=10000
EXPOSE $PORT

# Wait for MySQL to be ready, then migrate and start Gunicorn
CMD sh -c '\
  echo "Waiting for MySQL..."; \
  for i in $(seq 1 30); do \
    python -c "import pymysql; pymysql.connect(host=\"${DB_HOST:-mysql}\", port=int(\"${DB_PORT:-3306}\"), user=\"${DB_USER:-root}\", password=\"${DB_PASSWORD:-}\", db=\"${DB_NAME:-ecommerce_db}\")" 2>/dev/null && break; \
    echo "MySQL not ready, retrying ($i/30)..."; \
    sleep 2; \
  done; \
  echo "MySQL is ready! Running migrations..."; \
  python manage.py migrate && \
  gunicorn config.ecommerce.wsgi:application --bind 0.0.0.0:$PORT \
'
