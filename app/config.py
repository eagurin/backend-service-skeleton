from decouple import config

class Config:
    DEBUG: bool = config("DEBUG", default=True, cast=bool)
    HOST: str = config("HOST", default="localhost")
    PORT: int = config("PORT", default=8000, cast=int)
    DATABASE_URI: str = config(
        "DATABASE_URI", default="postgresql://user:password@localhost:5432/dbname"
    )
    RABBITMQ_URL: str = config(
        "RABBITMQ_URL", default="amqp://guest:guest@localhost:5672/"
    )
    RABBITMQ_QUEUE: str = config("RABBITMQ_QUEUE", default="transactions")
    REDIS_URL: str = config("REDIS_URL", default="redis://localhost:6379/0")
    REDIS_HOST: str = config('REDIS_HOST', default='localhost')
    REDIS_PORT: int = config('REDIS_PORT', default=6379, cast=int)
    REDIS_DB: int = config('REDIS_DB', default=0, cast=int)
