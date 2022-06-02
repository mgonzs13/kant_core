
""" Object Dto """

from typing import Any
from kant.kant_dto.dto import Dto
from kant.kant_dto.type_dto import TypeDto


class ObjectDto(Dto):
    """ Object Dto Class """

    def __init__(self, type: TypeDto, name: str) -> None:

        self.type = type
        self.name = name

        Dto.__init__(self)

    @property
    def type(self) -> TypeDto:
        return self._type

    @type.setter
    def type(self, type: TypeDto) -> None:
        self._type = type

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    def to_pddl(self) -> str:
        return self.name + " - " + self.type.name

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ObjectDto):
            return self.name == other.name

        return False
