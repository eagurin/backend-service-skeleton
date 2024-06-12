from typing import Any, Dict

from app.schemas import BaseSerializer


class TransactionSerializer(BaseSerializer):
    fields = ["amount", "uid", "timestamp"]

    def serialize(self) -> Dict[str, Any]:
        t_dict = super().serialize()
        t_dict["type"] = t_dict["type"].name
        return t_dict
