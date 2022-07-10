import os

from src.main import app


def get(key, default_value=None, coerce=lambda x: x):
    return coerce(os.getenv(key, default_value))


bind = get("GUNICORN_BIND", "0.0.0.0:8443")

certfile = get("GUNICORN_CERTFILE", "/app/certs/tls-localhost.crt")
keyfile = get("GUNICORN_KEYFILE", "/app/certs/tls-localhost.key")

workers = get("GUNICORN_WORKERS", 4, coerce=int)
worker_class = get("GUNICORN_WORKER_CLASS", "uvicorn.workers.UvicornWorker")

accesslog = get("GUNICORN_ACCESSLOG", "-")
errorlog = get("GUNICORN_ERRORLOG", "-")
loglevel = get("GUNICORN_LOGLEVEL", "info")

max_requests = get("GUNICORN_MAX_REQUESTS", 1000, coerce=int)
threads = get("GUNICORN_THREADS", 1, coerce=int)
timeout = get("GUNICORN_TIMEOUT", 30, coerce=int)
