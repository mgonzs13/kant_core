
""" Object Dao Interface """

from abc import abstractmethod
from kant.kant_dto import ObjectDto
from kant.kant_dao.dao_interface import Dao


class ObjectDao(Dao):
    """ Object Dao Interface Abstract Class"""

    @abstractmethod
    def get(self, object_name: str) -> ObjectDto:
        """ get a ObjectDto with a given object name
            return None if there is no with that object name

        Args:
            object_name (str): object name

        Returns:
            ObjectDto: ObjectDto of the object name
        """
