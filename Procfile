web: gunicorn --pythonpath src django_project.wsgi:application
worker: celery -A django_project worker -l info
beat: celery -A django_project beat --loglevel=info