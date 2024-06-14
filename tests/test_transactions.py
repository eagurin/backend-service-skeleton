from datetime import datetime
import requests

def test_transaction_2pc():
    user_resp = requests.post("http://localhost:8000/v1/user", json={"name": "petya"})
    assert user_resp.status_code == 201
    user = user_resp.json()
    user_id = user["id"]

    txn_data = {
        "user_id": user_id,
        "amount": "100.0",
        "type": "DEPOSIT",
        "timestamp": datetime.utcnow().isoformat(),
    }

    txn_resp = requests.post("http://localhost:8000/v1/transaction", json=txn_data)
    assert txn_resp.status_code == 201

    t_uid = txn_resp.json()["uid"]
    assert t_uid is not None

    txn_detail = requests.get(f"http://localhost:8000/v1/transaction/{t_uid}")
    assert txn_detail.status_code == 200
    assert txn_detail.json()["amount"] == "100.00"