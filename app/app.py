from aiohttp import web
from loguru import logger

from gino import Gino

db = Gino()

async def init_app():
    from .startups import init_services
    from .config import Config
    from .cleanups import close_services
    from .middlewares.error_handler import error_middleware
    from .api import setup_routes

    app = web.Application()

    app["config"] = Config
    app['db'] = db
    
    app.on_startup.append(init_services)
    
    app.on_cleanup.append(close_services)
    
    setup_routes(app)

    logger.info("Application initialized")
    return app
