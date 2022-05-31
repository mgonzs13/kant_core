
""" Dao Facory Interface """

from abc import ABC, abstractmethod
from kant.kant_dao.dao_interface import (
    TypeDao,
    ObjectDao,
    FluentDao,
    FactDao,
    ActionDao
)


class DaoFactory(ABC):
    """ Dao Facory Abstract Class """

    @abstractmethod
    def create_type_dao(self) -> TypeDao:
        """ create a dao type object

        Returns:
            TypeDao: dao for type
        """

    @abstractmethod
    def create_fluent_dao(self) -> FluentDao:
        """ create a dao fluent object

        Returns:
            FluentDao: dao for fluent
        """

    @abstractmethod
    def create_action_dao(self) -> ActionDao:
        """ create a dao action object

        Returns:
            ActionDao: dao for action
        """

    @abstractmethod
    def create_object_dao(self) -> ObjectDao:
        """ create a dao object object

        Returns:
            ObjectDao: dao for object
        """

    @abstractmethod
    def create_fact_dao(self) -> FactDao:
        """ create a dao type object

        Returns:
            FactDao: dao for fact
        """
