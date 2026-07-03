# Как запустить проект

### Шаг 1. Создание виртуального окружения
Нужно создать изолированную среду:
```bash
python -m venv venv
```
### Шаг 2. Установка зависимостей
```bash
pip install -r requirements.txt
```

### Шаг 3. Настройка файла .env (Секреты)
1. В корневой папке проекта создай файл и назови его строго **`.env`**
2. Вставь в него следующие настройки, но **укажи свой логин и пароль** от твоего локального PostgreSQL:

```env
SECRET_KEY=django-insecure-my-super-secret-key-123
DEBUG=True
DB_NAME=studguide
DB_USER=postgres
DB_PASSWORD=твой_пароль_от_бд_postgres
DB_HOST=127.0.0.1
DB_PORT=5432
```

### Шаг 4. Создание базы данных
На своем компьютере и создайте пустую базу данных с именем **`studguide`**.

### Шаг 5. Применение миграций
```bash
python manage.py migrate
```

### Шаг 6. Создание администратора
Чтобы ты мог зайти в админ-панель и создавать статьи, создай своего локального суперпользователя:
```bash
python manage.py createsuperuser
```

### Шаг 7. Запуск проекта!
```bash
python manage.py runserver
```
