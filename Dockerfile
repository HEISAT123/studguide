FROM python:3.13-slim

WORKDIR /app

# Устанавливаем системные зависимости для PostgreSQL
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Создаем папку для статики заранее
RUN mkdir -p staticfiles

# Даем права на выполнение скрипта
RUN chmod +x entrypoint.sh

# Запускаем через entrypoint
ENTRYPOINT ["./entrypoint.sh"]
