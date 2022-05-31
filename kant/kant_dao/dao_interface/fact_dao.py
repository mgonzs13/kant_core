
""" Proposition Dao Interface """

from abc import abstractmethod
from typing import List
from kant.kant_dto import FactDto
from kant.kant_dao.dao_interface import Dao


class FactDao(Dao):
    """ Proposition Dao Abstract Class """

    @abstractmethod
    def get_by_fluent(self, fluent_name: str) -> List[FactDto]:
        """ get all FactDto with a given fluent name

        Args:
            fluent_name (str): fluent name

        Returns:
            List[FactDto]: list of FactDto
        """

    @abstractmethod
    def get_goals(self) -> List[FactDto]:
        """ get all FactDto that are goals

        Returns:
            List[FactDto]: list of FactDto
        """

    @abstractmethod
    def get_no_goals(self) -> List[FactDto]:
        """ get all FactDto that are not goals

        Returns:
            List[FactDto]: list of FactDto
        """

    @abstractmethod
    def get_all(self) -> List[FactDto]:
        """ get all FactDto

        Returns:
            List[FactDto]: list of FactDto
        """

    @abstractmethod
    def get_propositions(self) -> List[FactDto]:
        """ get all propositions (facts with bool value)

        Returns:
            List[FactDto]: list of FactDto
        """

    @abstractmethod
    def get_functions(self) -> List[FactDto]:
        """ get all functions (facts with numeric value)

        Returns:
            List[FactDto]: list of FactDto
        """
