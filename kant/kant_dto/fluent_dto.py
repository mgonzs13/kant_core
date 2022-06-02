
""" Fluent Dto """

from typing import Any, List
from kant.kant_dto.dto import Dto
from kant.kant_dto.type_dto import TypeDto


class FluentDto(Dto):
    """ Fluent Dto Class """

    def __init__(self,
                 name: str,
                 types: List[TypeDto] = None,
                 is_numeric: bool = False
                 ) -> None:

        self.name = name
        self.types = types
        self.is_numeric = is_numeric

        Dto.__init__(self)

    @ property
    def name(self) -> str:
        return self._name

    @ name.setter
    def name(self, name: str) -> None:
        self._name = name

    @ property
    def types(self) -> List[TypeDto]:
        return self._types

    @ types.setter
    def types(self, types: List[TypeDto]) -> None:

        if types:
            self._types = types
        else:
            self._types = []

    @ property
    def is_numeric(self) -> bool:
        return self._is_numeric

    @ is_numeric.setter
    def is_numeric(self, is_numeric: bool) -> None:
        self._is_numeric = is_numeric

    def to_pddl(self) -> str:
        string = "(" + self.name

        if self.types:
            for i in range(len(self.types)):
                aux_type = self.types[i]
                type_name = aux_type.name
                string += " ?" + type_name[0] + str(i) + " - " + type_name

        string += ")"

        return string

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, FluentDto):
            return self.name == other.name

        return False
