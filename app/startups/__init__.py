from .database import init_db
from .rabbitmq import init_rabbitmq
from .redis import init_redis

async def init_services(app):
    await init_db(app)
    await init_rabbitmq(app)
    await init_redis(app)

__all__ = ["init_services"]
