from datetime import datetime
from aiohttp import web
from asyncpg import CheckViolationError
from app.models import TransactionType
from app.services import UserService, TransactionService
from app.schemas import UserCreate, UserResponse
from app.schemas import TransactionCreate, TransactionResponse
from loguru import logger
from pydantic import UUID4


user_service = UserService()
transaction_service = TransactionService()

async def add_user(request: web.Request) -> web.Response:
    """
    ---
    description: Создать нового пользователя.
    tags:
    - Пользователи
    produces:
    - application/json
    parameters:
    - name: body
      in: body
      description: Данные нового пользователя
      required: true
      schema:
        UserCreate
    responses:
      "201":
        description: Успешное создание пользователя
    """
    request_data = await request.json()
    user_create = UserCreate(**request_data)
    user = await user_service.create_user(user_create)
    logger.info(f"User created with id: {user.id}")
    user_response = UserResponse(id=user.id, name=user.name, balance=str(user.balance))
    return web.json_response(user_response.dict(), status=201)

async def get_user(request: web.Request) -> web.Response:
    """
    ---
    description: Получить данные пользователя.
    tags:
    - Пользователи
    produces:
    - application/json
    parameters:
    - name: id
      in: path
      required: true
      type: string
      description: UID пользователя
    responses:
      "200":
        description: Успешное получение данных пользователя
      "404":
        description: Пользователь не найден
    """
    user_id = int(request.match_info["id"])
    timestamp_str = request.query.get("date")
    timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else None

    user, user_transactions = await user_service.get_user_with_transactions(request.app, user_id, timestamp)

    if not user:
        logger.warning(f"User with id: {user_id} not found")
        return web.json_response(status=404)

    balance = None
    if timestamp:
        balance = sum([t.amount if t.type == TransactionType.DEPOSIT else -abs(t.amount) for t in user_transactions])
        balance = "%.2f" % balance

    serialized_user = UserResponse(
        id=user.id, 
        name=user.name, 
        balance=balance if balance is not None else str(user.balance)
    )

    logger.info(f"User data retrieved for id: {user_id}")
    return web.json_response(serialized_user.dict(), status=200)

async def add_transaction(request: web.Request) -> web.Response:
    """
    ---
    description: Добавить новую транзакцию.
    tags:
    - Транзакции
    produces:
    - application/json
    parameters:
    - name: body
      in: body
      description: Данные новой транзакции
      required: true
      schema:
        TransactionCreate
    responses:
      "201":
        description: Успешное добавление транзакции
      "402":
        description: Недостаточно средств
    """
    request_data = await request.json()
    transaction_create = TransactionCreate(**request_data)
    
    async with request.app["db"].transaction() as tx:
        try:
            await user_service.update_user_balance(transaction_create)
        except CheckViolationError:
            logger.error(f"Insufficient funds for user_id: {transaction_create.user_id}")
            return web.json_response(status=402)
        
        transaction = await transaction_service.create_transaction(transaction_create)
        transaction_response = TransactionResponse(
            uid=transaction.uid,
            type=transaction.type.name,
            amount=str(transaction.amount),
            timestamp=transaction.timestamp,
            user_id=transaction.user_id,
        )
        logger.info(f"Transaction created with id: {transaction.uid}")
        return web.json_response(transaction_response.dict(), status=201)

async def get_transaction(request: web.Request) -> web.Response:
    """
    ---
    description: Получить данные транзакции.
    tags:
    - Транзакции
    produces:
    - application/json
    parameters:
    - name: uid
      in: path
      required: true
      type: string
      description: UID транзакции
    responses:
      "200":
        description: Успешное получение данных транзакции
      "404":
        description: Транзакция не найдена
    """
    transaction_uid = UUID4(request.match_info["uid"])
    transaction = await transaction_service.get_transaction(transaction_uid)

    if not transaction:
        logger.warning(f"Transaction with uid: {transaction_uid} not found")
        return web.json_response(status=404)
    
    transaction_response = TransactionResponse(
        uid=transaction.uid,
        type=transaction.type.name,
        amount=str(transaction.amount),
        timestamp=transaction.timestamp,
        user_id=transaction.user_id
    )
    logger.info(f"Transaction data retrieved for uid: {transaction_uid}")
    return web.json_response(transaction_response.dict(), status=200)

def setup_routes(app: web.Application):
    app.router.add_route("GET", r"/v1/user/{id}", get_user, name="get_user")
    app.router.add_route("POST", r"/v1/user", add_user, name="add_user")
    app.router.add_route("GET", r"/v1/transaction/{uid}", get_transaction, name="get_transaction")
    app.router.add_route("POST", r"/v1/transaction", add_transaction, name="add_transaction")
