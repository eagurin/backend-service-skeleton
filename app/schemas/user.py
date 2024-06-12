from app.schemas import BaseSerializer


class UserSerializer(BaseSerializer):
    fields = ["balance"]
