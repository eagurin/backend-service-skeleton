from typing import Any, Dict, List, Union

from app.models import Transaction, User


class BaseSerializer:
    fields: List[str]

    def __init__(self, obj: Union[User, Transaction]):
        self.obj = obj

    def serialize(self) -> Dict[str, Any]:
        model_dict = self.obj.to_dict()
        for f in self.fields:
            model_dict[f] = str(model_dict[f])
        return model_dict
