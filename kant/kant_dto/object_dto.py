
""" Object Dto """

from typing import Any
from kant.kant_dto.dto import Dto
from kant.kant_dto.type_dto import TypeDto


class ObjectDto(Dto):
    """ Object Dto Class """

    def __init__(self, type: TypeDto, name: str) -> None:

        self.set_type(type)
        self.set_name(name)

        Dto.__init__(self)

    def get_type(self) -> TypeDto:
        """ type getter

        Returns:
            TypeDto: type
        """

        return self._type

    def set_type(self, type: TypeDto) -> None:
        """ type setter

        Args:
            type (TypeDto): type
        """

        self._type = type

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

    def __str__(self) -> str:
        return self._name + " - " + self._type.get_name()

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ObjectDto):
            return self.get_name() == other.get_name()

        return False
