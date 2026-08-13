FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

#
# System dependencies
#


RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    libpq-dev \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    shared-mime-info \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*


#
# Create app user
#

RUN groupadd -r appgroup && \
    useradd -r -g appgroup appuser

#
# Python dependencies
#

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install \
    --no-cache-dir \
    -r requirements.txt

#
# Copy application
#

COPY . .

#
# Entrypoint
#

COPY entrypoint.sh /app/entrypoint.sh

RUN chmod +x /app/entrypoint.sh

#
# Create runtime folders
#

RUN mkdir -p \
    uploads \
    uploads/imports \
    generated \
    generated/pdfs \
    generated/csv \
    generated/barcodes \
    generated/exports \
    backups \
    logs

RUN chown -R appuser:appgroup /app

USER appuser

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

EXPOSE 5000

HEALTHCHECK \
    --interval=30s \
    --timeout=10s \
    --start-period=30s \
    --retries=5 \
    CMD curl -f http://localhost:5000/health/live || exit 1

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--threads", "4", "--timeout", "120", "app:app"]