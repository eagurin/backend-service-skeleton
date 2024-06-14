from app import db
from loguru import logger

async def init_db(app):
    try:
        await db.set_bind(app['config'].DATABASE_URI)
        await db.gino.create_all()
        app['db'] = db
        logger.info("Database connection established")
    except Exception as e:
        logger.error(f"Failed to connect to the database: {e}")
        raise e
