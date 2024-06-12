from decouple import config

class Config:
    DEBUG: bool = config('DEBUG', default=False, cast=bool)
    HOST: str = config('HOST', default='0.0.0.0')
    PORT: int = config('PORT', default=8000, cast=int)
    DATABASE_URI: str = config('DATABASE_URI', default='postgres://user:password@localhost/dbname')
    RABBITMQ_URL: str = config('RABBITMQ_URL', default='amqp://guest:guest@localhost/')
    RABBITMQ_QUEUE: str = config('RABBITMQ_QUEUE', default='transactions')