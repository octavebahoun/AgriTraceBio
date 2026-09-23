FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && apt-get install -y --no-install-recommends \
      libjpeg62-turbo libfreetype6 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY config.py app.py ./
COPY src/ ./src/

RUN adduser --disabled-password --gecos "" --uid 1001 agritrace \
    && mkdir -p /app/uploads && chown -R agritrace:agritrace /app
USER agritrace

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=5s --retries=3 --start-period=15s \
  CMD python -c "import urllib.request; \
    urllib.request.urlopen('http://127.0.0.1:5000/api/health', timeout=3)" \
    || exit 1

CMD ["gunicorn", "--bind", "0.0.0.0:5000", \
     "--workers", "2", "--threads", "4", \
     "--timeout", "60", "app:app"]
