# Финансовый сервис на базе Aiohttp

Этот проект представляет собой финансовый сервис, разработанный с использованием Aiohttp, который предоставляет API для управления пользователями и их транзакциями. Основные функции включают создание пользователей, выполнение транзакций (депозиты и снятия) и получение информации о пользователях и транзакциях.

### Основные аспекты реализации

1. **Горизонтальное масштабирование**:
   - Использование балансировщиков нагрузки для распределения запросов.
   - Разделение данных по шардам или использование кластерных баз данных.
   - Кэширование с помощью Redis для снижения нагрузки на базу данных.

2. **Обеспечение обработки транзакций ровно один раз**:
   - Идемпотентные операции с уникальными идентификаторами транзакций.
   - Использование брокеров сообщений (RabbitMQ) для гарантированной доставки.

3. **Идемпотентность операций**:
   - Уникальные идентификаторы для транзакций.
   - Проверка состояния системы перед выполнением операции.

4. **Атомарность транзакций**:
   - Использование транзакций базы данных.
   - Протокол двухфазного коммита (2PC) для распределенных систем.

5. **Дедупликация сообщений**:
   - Уникальные идентификаторы транзакций.
   - Хранилище состояния для отслеживания обработанных сообщений.

### Стек технологий

- **Python и aiohttp**: Для создания асинхронного веб-сервера.
- **PostgreSQL и Gino**: Для работы с базой данных.
- **RabbitMQ**: Для обмена сообщениями между сервисами.
- **Redis**: Для кэширования и дедупликации сообщений.

## Гарантия обработки транзакции ровно один раз

Для обеспечения обработки транзакции ровно один раз необходимо использовать механизм транзакций базы данных и очередей сообщений. В данном проекте используется RabbitMQ для обработки транзакций. Основные требования:

- **Использование (Working with RabbitMQ transactions) в RabbitMQ**: Это гарантирует, что сообщение будет удалено из очереди только после успешной обработки.
- **Обработка транзакций в рамках одной транзакции базы данных и очереди сообщений**: Это гарантирует атомарность операции.
- **Использование уникальных идентификаторов транзакций для предотвращения повторной обработки**: Все транзакции должны иметь уникальные идентификаторы (UUID), чтобы избежать дублирования.

Пример кода для обработки транзакций с RabbitMQ:

```python
import asyncio

import aio_pika

connection = await aio_pika.connect_robust(
    "amqp://guest:guest@127.0.0.1/",
)

async with connection:
    routing_key = "test_queue"

    # Transactions conflicts with `publisher_confirms`
    channel = await connection.channel(publisher_confirms=False)

    # Use transactions with async context manager
    async with channel.transaction():
        # Publishing messages but delivery will not be done
        # before committing this transaction
        for i in range(10):
            message = aio_pika.Message(body="Hello #{}".format(i).encode())

            await channel.default_exchange.publish(
                message, routing_key=routing_key,
            )

    # Using transactions manually
    tx = channel.transaction()

    # start transaction manually
    await tx.select()

    await channel.default_exchange.publish(
        aio_pika.Message(body="Hello {}".format(routing_key).encode()),
        routing_key=routing_key,
    )

    await tx.commit()

    # Using transactions manually
    tx = channel.transaction()

    # start transaction manually
    await tx.select()

    await channel.default_exchange.publish(
        aio_pika.Message(body="Should be rejected".encode()),
        routing_key=routing_key,
    )

    await tx.rollback()
```

## Уведомление других сервисов о транзакциях

Для уведомления других сервисов о транзакциях можно использовать механизмы публикации/подписки (publish/subscribe). Например, при выполнении транзакции публиковать сообщение в RabbitMQ, которое будет обработано другим сервисом (например, рекламным движком).

## Контроль качества работы сервиса

Для контроля качества работы сервиса можно использовать следующие инструменты:

- **Мониторинг и логирование**:
  - Prometheus и Grafana для мониторинга метрик.
  - Loguru для логирования.

- **Трассировка**:
  - Jaeger для распределенной трассировки запросов.

- **Тестирование**:
  - Pytest для написания юнит-тестов и интеграционных тестов.

- **CI/CD**:
  - GitHub Actions или GitLab CI для автоматического тестирования и деплоя.

## Запуск проекта

1. Создайте файл `.env` в корне проекта и добавьте следующие переменные окружения:

```env
DEBUG=True
HOST=0.0.0.0
PORT=8000
DATABASE_URI=postgres://user:password@localhost/dbname
RABBITMQ_URL=amqp://guest:guest@localhost/
RABBITMQ_QUEUE=transactions
```

2. Docker:

```bash
docker-compose up -d --build
```

3. Migrations:

```bash
alembic upgrade head
```

## Project Structure (in dev)

```plaintext
backend-service-skeleton/
    app/
        config.py
        __init__.py
        __main__.py
        api/
            __init__.py
            routes.py
        models/
            __init__.py
            user.py
            transaction.py
        schemas/
            __init__.py
            user.py
            transaction.py
        services/
            __init__.py
            user_service.py
            transaction_service.py
            messaging_service.py
            cache_service.py
        middlewares/
            __init__.py
            error_handler.py
        startups/
            __init__.py
            database.py
            rabbitmq.py
            redis.py
            cache.py
        cleanups/
            __init__.py
            database.py
            rabbitmq.py
            redis.py
            cache.py
```
