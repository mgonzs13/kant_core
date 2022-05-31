
""" Type Dao Interface """

from abc import abstractmethod
from kant.kant_dto import TypeDto
from kant.kant_dao.dao_interface import Dao


class TypeDao(Dao):
    """ Type Dao Abstract Class """

    @abstractmethod
    def get(self, type_name: str) -> TypeDto:
        """ get a TypeDto with a given type name
            return None if there is no with that type name

        Args:
            type_name (str): type name

        Returns:
            TypeDto: TypeDto of the type name
        """
