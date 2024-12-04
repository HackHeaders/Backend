#!/usr/bin/env bash
# Sai do script se houver algum erro
set -o errexit

# Atualiza o pip
pip install --upgrade pip

# Instala as dependências
pip install -r requirements.txt

python manage.py collectstatic --no-input

# Aplica as migrações
python manage.py migrate

if ! celery -A config.celery worker --loglevel=info --logfile=/var/log/celery/celery.log &; then
    echo "Falha ao iniciar o Celery"
    exit 1
fi