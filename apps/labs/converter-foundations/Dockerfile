# syntax=docker/dockerfile:1

FROM python:3.12-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install dependencies first so the layer is cached across code changes.
COPY requirements.lock ./
RUN pip install -r requirements.lock

# Application code and static assets.
COPY app.py gunicorn.conf.py ./
COPY i18n.py ./
COPY models/ ./models/
COPY layouts/ ./layouts/
COPY callbacks/ ./callbacks/
COPY assets/ ./assets/

# Run as an unprivileged user.
RUN useradd --system --uid 10001 --home-dir /app --no-create-home appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 8050

# Liveness check against the app's own /healthz route.
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD ["python", "-c", "import urllib.request,sys; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8050/healthz', timeout=4).status==200 else 1)"]

CMD ["gunicorn", "app:server", "-c", "gunicorn.conf.py"]
