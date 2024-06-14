from .database import close_db
from .rabbitmq import close_rabbitmq
from .redis import close_redis

async def close_services(app):
    await close_db(app)
    await close_rabbitmq(app)
    await close_redis(app)

__all__ = ["close_services"]
