
""" Type Dto """

from typing import Any
from kant.kant_dto.dto import Dto


class TypeDto(Dto):
    """ Type Dto Class """

    def __init__(self, name: str, father: "TypeDto" = None) -> None:

        self.name = name
        self.father = father

        Dto.__init__(self)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def father(self) -> "TypeDto":
        return self._father

    @father.setter
    def father(self, father: "TypeDto") -> None:
        self._father = father

    def to_pddl(self) -> str:

        if self.father is None:
            return self.name

        return self.name + " - " + self.father.name

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, TypeDto):
            return self.name == other.name

        return False
