# prosesing_service_task
Processing Service

Сервис обработки событий с использованием очередей сообщений (RabbitMQ) и паттерна Outbox.

Возможности
асинхронная обработка событий
публикация событий в очередь (publisher)
потребление событий (consumer)
retry механизм при недоступности RabbitMQ
использование паттерна Outbox
PostgreSQL хранение данных
Alembic миграции
Docker запуск
Основные компоненты

API:

запуск веб-сервиса
работа с БД
создание событий

Publisher:

отправка событий в RabbitMQ
retry при ошибках

Consumer:

получение сообщений из очереди
обработка бизнес-логики

Broker (RabbitMQ):

очередь сообщений
маршрутизация событий

Database:

PostgreSQL
таблица outbox

Запуск через Docker
```bach
docker compose up --build
```

ТЗ: 
https://docs.360.yandex.ru/docs/view?url=ya-disk-public%3A%2F%2FAapA2ka%2BiiSJVWmR3HJ%2FH16YZIep9USPsfewdC2X1kCtChv54CucGLB7vG3eId1WsLK2WbwBkR%2F%2FqfmVHoPilw%3D%3D%3A%2F%D0%A2%D0%B5%D1%81%D1%82%D0%BE%D0%B2%D0%BE%D0%B5%20(1).pdf&name=%D0%A2%D0%B5%D1%81%D1%82%D0%BE%D0%B2%D0%BE%D0%B5%20(1).pdf

