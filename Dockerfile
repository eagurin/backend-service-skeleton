# Базовый образ для Python
FROM python:3.11-slim AS python-base

# Установка переменных окружения
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.5.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# Добавление Poetry и виртуального окружения в PATH
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Установка необходимых пакетов и Poetry
RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && poetry --version

# Слой сборки зависимостей
FROM python-base AS builder

# Установка рабочего каталога
WORKDIR $PYSETUP_PATH

# Копирование файлов зависимостей
COPY pyproject.toml poetry.lock ./

# Установка зависимостей без dev-пакетов
RUN poetry install --no-dev

# Копирование остальных файлов проекта
COPY . .

# Финальный слой для разработки
FROM python-base AS development

# Установка переменных окружения
ENV APP_ENV=development

# Копирование установленных зависимостей и файлов проекта из слоя сборки
COPY --from=builder $POETRY_HOME $POETRY_HOME
COPY --from=builder $PYSETUP_PATH $PYSETUP_PATH

# Установка рабочего каталога
WORKDIR $PYSETUP_PATH

# Открытие порта для приложения
EXPOSE 8000

# Команда для запуска приложения в режиме разработки
CMD ["poetry", "run", "python", "-m", "aiohttp.web", "-H", "0.0.0.0", "-P", "8000", "app.__main__:create_app_wrapper"]

# # Финальный слой для продакшена
# FROM python-base AS production

# # Установка переменных окружения
# ENV APP_ENV=production

# # Копирование установленных зависимостей и файлов проекта из слоя сборки
# COPY --from=builder $POETRY_HOME $POETRY_HOME
# COPY --from=builder $PYSETUP_PATH $PYSETUP_PATH

# # Установка рабочего каталога
# WORKDIR $PYSETUP_PATH

# # Команда для запуска приложения в режиме продакшена
# CMD ["poetry", "run", "gunicorn", "-b", "0.0.0.0:8000", "app.__main__:create_app_wrapper", "-k", "aiohttp.GunicornWebWorker"]
