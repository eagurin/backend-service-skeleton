from typing import Dict, Any, Union, List

from app.models import User, Transaction


class BaseSerializer:
    fields: List[str]

    def __init__(self, obj: Union[User, Transaction]):
        self.obj = obj

    def serialize(self) -> Dict[str, Any]:
        model_dict = self.obj.to_dict()
        for f in self.fields:
            model_dict[f] = str(model_dict[f])
        return model_dict


class UserSerializer(BaseSerializer):
    fields = ["balance"]


class TransactionSerializer(BaseSerializer):
    fields = ["amount", "uid", "timestamp"]

    def serialize(self) -> Dict[str, Any]:
        t_dict = super().serialize()
        t_dict["type"] = t_dict["type"].name
        return t_dict
