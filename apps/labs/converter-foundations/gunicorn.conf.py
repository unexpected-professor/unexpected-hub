"""Gunicorn configuration for the Converter Foundations laboratory.

These values are a conservative starting point, not a measured capacity
guarantee. They must be revisited after the representative-classroom load test
(hub UPH-026): each worker holds its own copy of NumPy/Plotly and the callback
work is CPU-bound, so raising `workers` trades memory for concurrency.

Every setting can be overridden by an environment variable of the same
upper-case name (e.g. WEB_CONCURRENCY, GUNICORN_TIMEOUT).
"""

import os

bind = os.environ.get('GUNICORN_BIND', '0.0.0.0:8050')

# 2 sync-ish workers fit a 4 GB host that also runs the static site + proxy.
workers = int(os.environ.get('WEB_CONCURRENCY', '2'))
worker_class = os.environ.get('GUNICORN_WORKER_CLASS', 'gthread')
threads = int(os.environ.get('GUNICORN_THREADS', '4'))

# Dash callbacks are short; a long timeout only hides a stuck worker.
timeout = int(os.environ.get('GUNICORN_TIMEOUT', '60'))
graceful_timeout = int(os.environ.get('GUNICORN_GRACEFUL_TIMEOUT', '30'))
keepalive = int(os.environ.get('GUNICORN_KEEPALIVE', '5'))

# Recycle workers periodically to bound memory growth.
max_requests = int(os.environ.get('GUNICORN_MAX_REQUESTS', '2000'))
max_requests_jitter = int(os.environ.get('GUNICORN_MAX_REQUESTS_JITTER', '200'))

# Logs go to stdout/stderr for the container runtime to collect.
accesslog = '-'
errorlog = '-'
loglevel = os.environ.get('GUNICORN_LOG_LEVEL', 'info')

# Trust the reverse proxy in front of the container for scheme/host headers.
forwarded_allow_ips = os.environ.get('FORWARDED_ALLOW_IPS', '*')
