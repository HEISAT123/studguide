#!/bin/sh

# Прерывать выполнение при любой ошибке
set -e

echo "Сборка статики (collectstatic)..."
python manage.py collectstatic --noinput

echo "Применение миграций базы данных..."
python manage.py migrate --noinput

echo "Запуск Gunicorn..."
# exec заменяет процесс bash на gunicorn, чтобы он корректно получал системные сигналы (например, при остановке контейнера)
exec gunicorn --bind 0.0.0.0:8000 config.wsgi:application