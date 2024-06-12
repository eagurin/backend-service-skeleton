import uvloop
from aiohttp import web
from dotenv import load_dotenv
from loguru import logger
import asyncio

from app.app import init_app

load_dotenv()

def create_app() -> web.Application:
    uvloop.install()
    return init_app()

def create_app_wrapper(argv=None):
    return create_app()

if __name__ == "__main__":
    asyncio.run(create_app())
    app = asyncio.run(create_app())
    logger.info("Starting application")
    web.run_app(app, host=app["config"].HOST, port=app["config"].PORT)
