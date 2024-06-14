import asyncio
import uvloop
from aiohttp import web
from loguru import logger
from app.app import init_app

async def create_app(argv=None) -> web.Application:
    uvloop.install()
    return await init_app()

if __name__ == "__main__":
    try:
        logger.info("Creating application")
        app = asyncio.run(create_app())
        logger.info("Starting application")
        web.run_app(app, host=app["config"].HOST, port=app["config"].PORT)
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        raise e