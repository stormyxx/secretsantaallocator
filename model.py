from typing import List, Tuple

from attr import define


@define(frozen=True)
class User:
    name: str
    can_give: Tuple[str, ...]
    can_receive: Tuple[str, ...]


@define
class Allocation:
    giver: User
    receiver: User

    def __str__(self) -> str:
        return f"{self.giver.name} -> {self.receiver.name}"
