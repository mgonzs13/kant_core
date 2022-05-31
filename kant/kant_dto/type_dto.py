
""" Type Dto """

from typing import Any
from kant.kant_dto.dto import Dto


class TypeDto(Dto):
    """ Type Dto Class """

    def __init__(self, name: str, father: "TypeDto" = None) -> None:

        self.set_name(name)
        self.set_father(father)

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

    def get_father(self) -> "TypeDto":
        """ father getter

        Returns:
            TypeDto: name
        """

        return self._father

    def set_father(self, father: "TypeDto") -> None:
        """ father setter

        Args:
            name (TypeDto): name
        """

        self._father = father

    def __str__(self) -> str:

        if self._father is None:
            return self._name

        return self._name + " - " + self._father.get_name()

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, TypeDto):
            return self.get_name() == other.get_name()

        return False
