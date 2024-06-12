from aiohttp import web
from gino import Gino

app = web.Application()

db = Gino()


def init_app() -> web.Application:
    from app.api.routes import add_routes

    from .cleanups import close_db
    from .config import Config
    from .startups import init_db

    app["config"] = Config
    app["db"] = db

    # Startups
    app.on_startup.append(init_db)

    # Cleanups
    app.on_cleanup.append(close_db)
    add_routes(app)

    return app
