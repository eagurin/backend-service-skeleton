from datetime import datetime
import requests
import uuid

def assert_balance(user, expected_balance, date=None):
    """
    Helper function to assert the balance of a user.
    """
    url = f'http://localhost:8000/v1/user/{user["id"]}'
    if date:
        url += f"?date={date}"
    balance_resp = requests.get(url)
    assert balance_resp.status_code == 200
    assert balance_resp.json()["balance"] == expected_balance

def test_transaction_deduplication():
    """
    Test for transaction deduplication ensuring that the same transaction
    cannot be processed multiple times.
    """
    # Create a new user
    user_resp = requests.post("http://localhost:8000/v1/user", json={"name": "petya"})
    assert user_resp.status_code == 201
    user = user_resp.json()
    user_id = user["id"]
    assert user_id is not None
    assert user["name"] == "petya"

    # Initial balance check
    assert_balance(user, "0.00")

    # Create a transaction
    txn_id = str(uuid.uuid4())
    txn_data = {
        "uid": txn_id,
        "type": "DEPOSIT",
        "amount": "100.0",
        "timestamp": datetime.utcnow().isoformat(),
        "user_id": user_id,
    }
    txn_resp = requests.post("http://localhost:8000/v1/transaction", json=txn_data)
    assert txn_resp.status_code == 201
    assert_balance(user, "100.00")

    # Attempt to create the same transaction again
    duplicate_txn_resp = requests.post("http://localhost:8000/v1/transaction", json=txn_data)
    assert duplicate_txn_resp.status_code == 400  # or appropriate status code for duplicate
    
    # Final balance check to ensure no duplicate transaction was processed
    assert_balance(user, "100.00")

test_transaction_deduplication()
