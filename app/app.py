from aiohttp import web
from gino import Gino


app = web.Application()

db = Gino()


def init_app() -> web.Application:
    from .config import Config
    from .cleanups import close_db
    from .startups import init_db
    from app.api.routes import add_routes

    app["config"] = Config
    app["db"] = db

    # Startups
    app.on_startup.append(init_db)

    # Cleanups
    app.on_cleanup.append(close_db)
    add_routes(app)

    return app
