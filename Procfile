web: gunicorn config.asgi:application -k uvicorn.workers.UvicornWorker
worker: celery -A config.celery worker -l info
beat: celery -A config.celery beat --loglevel=info