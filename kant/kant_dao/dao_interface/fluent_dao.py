
""" Predicate Dao Interface """

from abc import abstractmethod
from kant.kant_dto import FluentDto
from kant.kant_dao.dao_interface import Dao


class FluentDao(Dao):
    """ Predicate Dao Abstract Class """

    @abstractmethod
    def get(self, predicate_name: str) -> FluentDto:
        """ get a FluentDto with a given predicate name
            return None if there is no with that predicate name

        Args:
            predicate_name (str): predicate name

        Returns:
            FluentDto: FluentDto of the predicate name
        """
