web: gunicorn --pythonpath config.wsgi:application
worker: celery -A config.celery worker -l info
beat: celery -A config.celery beat --loglevel=info