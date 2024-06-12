from aiohttp import web

from app.schemas.transaction import TransactionSerializer
from app.schemas.user import UserSerializer
from app.services.transaction_service import TransactionService
from app.services.user_service import UserService

user_service = UserService()
transaction_service = TransactionService()


async def add_user(request: web.Request) -> web.Response:
    request_json = await request.json()
    user = await user_service.create_user(**request_json)
    return web.json_response(UserSerializer(user).serialize(), status=201)


async def add_transaction(request: web.Request) -> web.Response:
    request_json = await request.json()
    amount = request_json["amount"]
    user_id = request_json["user_id"]
    transaction_type = request_json["type"]
    try:
        await user_service.update_user_balance(
            amount, user_id, transaction_type
        )
    except ValueError as e:
        return web.json_response({"error": str(e)}, status=402)

    transaction = await transaction_service.create_transaction(request_json)
    return web.json_response(
        TransactionSerializer(transaction).serialize(), status=201
    )


async def get_user(request: web.Request) -> web.Response:
    user_id = int(request.match_info["id"])
    timestamp = request.query.get("date")
    user, user_transactions = await user_service.get_user_with_transaction(
        user_id=user_id, timestamp=timestamp
    )
    if not user:
        return web.json_response(status=404)
    balance = user_service.calculate_balance(user_transactions)
    serialized = UserSerializer(user).serialize()
    serialized["balance"] = balance
    return web.json_response(serialized, status=200)


async def get_transaction(request: web.Request) -> web.Response:
    transaction_uid = request.match_info["uid"]
    transaction = await transaction_service.get_transaction(transaction_uid)
    if not transaction:
        return web.json_response(status=404)
    return web.json_response(
        TransactionSerializer(transaction).serialize(), status=200
    )


def add_routes(app):
    app.router.add_route("GET", r"/v1/user/{id}", get_user, name="get_user")
    app.router.add_route("POST", r"/v1/user", add_user, name="add_user")
    app.router.add_route(
        "GET",
        r"/v1/transaction/{uid}",
        get_transaction,
        name="get_transaction",
    )
    app.router.add_route(
        "POST", r"/v1/transaction", add_transaction, name="add_transaction"
    )
