from aiohttp import web
from app.models import db

async def init_app() -> web.Application:
    from app.api.routes import add_routes
    from .cleanups import close_db
    from .config import Config
    from .startups import init_db
    from app.middlewares.error_handler import error_middleware

    app = web.Application(middlewares=[error_middleware])

    app = web.Application()

    app["config"] = Config
    app["db"] = db

    # Startups
    app.on_startup.append(init_db)

    # Cleanups
    app.on_cleanup.append(close_db)
    add_routes(app)

    return app
