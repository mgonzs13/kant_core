
""" Dto Abstract Class """

from abc import ABC, abstractmethod


class Dto(ABC):
    """ Dto Abstract Class """

    @abstractmethod
    def to_pddl(self) -> str:
        """ generate PDDL text for this DTO

        Returns:
            str: PDDL text
        """

    def __str__(self) -> str:
        return self.to_pddl()

    @abstractmethod
    def __eq__(self, other) -> bool:
        """ equals DTO

        Args:
            other (_type_): other DTO

        Returns:
            bool: equals?
        """
