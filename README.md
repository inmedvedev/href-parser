# Парсер ссылок

Скрипт анализирует любую web-страницу и составляет таблицу с найденными ссылками и [инофрмацией о доменах.](https://api.domainsdb.info/v1/)

## Как запустить

Скачайте код, перейдите в каталог проекта,
создайте виртуальное окружение 

```sh
python3 -m venv venv
```
Активируйте его. На разных операционных системах это делается разными командами:
- Windows: `.\venv\Scripts\activate`
- MacOS/Linux: `source venv/bin/activate`


Установите зависимости в виртуальное окружение:
```sh
pip install -r requirements.txt
```
Создайте файл базы данных SQLite(Важно: версия должна быть 3.35+) и отмигрируйте её следующей командой:


```sh
python manage.py migrate
```

Запустите сервер:

```sh
python manage.py runserver
```
Запустите воркер Celery:
```sh
celery -A href_parser worker -l INFO
```
Опционально мониторинг созданных задач:
```sh
celery -A href_parser flower
```
