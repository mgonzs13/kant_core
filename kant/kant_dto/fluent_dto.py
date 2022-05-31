
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

        self.set_name(name)
        self.set_types(types)
        self.set_is_numeric(is_numeric)

        Dto.__init__(self)

    def get_name(self) -> str:
        """ name getter

        Returns:
            str: name
        """

        return self._name

    def set_name(self, name: str) -> None:
        """ name setter

        Args:
            name (str): name
        """

        self._name = name

    def get_types(self) -> List[TypeDto]:
        """ types list getter

        Returns:
            List[TypeDto]: list of types
        """

        return self._types

    def set_types(self, types: List[TypeDto]) -> None:
        """ types list setter

        Args:
            types (List[TypeDto]): list of types
        """

        if types:
            self._types = types
        else:
            self._types = []

    def get_is_numeric(self) -> bool:
        """ is numeric getter

        Returns:
            bool: is numeric?
        """

        return self._is_numeric

    def set_is_numeric(self, is_numeric: bool) -> None:
        """ is numeric setter

        Args:
            is_numeric (int): is numeric?
        """

        self._is_numeric = is_numeric

    def __str__(self) -> str:
        string = "(" + self._name

        if self._types:
            for i in range(len(self._types)):
                aux_type = self._types[i]
                type_name = aux_type.get_name()
                string += " ?" + type_name[0] + str(i) + " - " + type_name

        string += ")"

        return string

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, FluentDto):
            return self.get_name() == other.get_name()

        return False
