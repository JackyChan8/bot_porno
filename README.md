# Default Проект для Aiogram

## Миграции

1. Создание миграции:
```shell
alembic revision --autogenerate -m "Migration Comment"
```
2. Применить миграции
```shell
alembic upgrade head
```

## Запуск Проекта
```shell
docker compose up --build
```