from enum import Enum


class Status(str, Enum):
    first = "в обработке"
    second = "готовится"
    third = "доставляется"


def next_status(status: str):
    status = status.lower()
    if status == Status.first:
        return Status.second
    elif status == Status.second:
        return Status.third
    else:
        raise ValueError(f"{status} is not a valid status")