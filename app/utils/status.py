from enum import Enum


class Status(str, Enum):
    first = "в обработке"
    second = "готовится"
    third = "доставляется"

    def next(self):
        members = list(Status)
        idx = members.index(self)
        if idx + 1 < len(members):
            return members[idx + 1]
        return "Доставлен"

