from aiohttp import web
from loguru import logger

@web.middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
        if response.status == 404:
            return web.json_response({"error": "Not found"}, status=404)
        return response
        
    except web.HTTPException as ex:
        if ex.status == 404:
            return web.json_response({"error": "Not found"}, status=404)
        raise ex
    except Exception as ex:
        logger.exception("An unexpected error occurred")
        return web.json_response({"error": "Internal Server Error"}, status=500)