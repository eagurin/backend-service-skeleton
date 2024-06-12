from aiohttp import web
from aiohttp.web_middlewares import middleware

from app.utils.time_utils import InvalidTimestampError


@middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
        if response.status == 404:
            return web.json_response({"error": "Not found"}, status=404)
        return response
    except web.HTTPException as ex:
        if ex.status == 404:
            return web.json_response({"error": "Not found"}, status=404)
        raise
    except InvalidTimestampError as e:
        return web.json_response({"error": str(e)}, status=400)
    except Exception as e:
        return web.json_response({"error": str(e)}, status=500)
