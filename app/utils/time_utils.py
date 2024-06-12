import datetime
from typing import Optional, Union


class InvalidTimestampError(Exception):
    pass


def get_current_time() -> datetime.datetime:
    return datetime.datetime.now()


def parse_timestamp(
    timestamp: Optional[Union[str, datetime.datetime]]
) -> datetime.datetime:
    if isinstance(timestamp, str):
        timestamp = datetime.datetime.fromisoformat(timestamp)
    elif not timestamp:
        timestamp = get_current_time()
    validate_timestamp(timestamp)
    return timestamp


def validate_timestamp(timestamp: datetime.datetime) -> None:
    if timestamp > get_current_time():
        raise InvalidTimestampError("Timestamp cannot be in the future")
