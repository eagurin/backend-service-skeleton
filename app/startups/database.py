from aiohttp import web


async def init_db(app: web.Application) -> None:
    await app["db"].set_bind(app["config"].DATABASE_URI)
