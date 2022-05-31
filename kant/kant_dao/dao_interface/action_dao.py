
""" Action Dao Interface """

from abc import abstractmethod
from kant.kant_dto import ActionDto
from kant.kant_dao.dao_interface import Dao


class ActionDao(Dao):
    """ Action Dao Abstract Class """

    @abstractmethod
    def get(self, action_name: str) -> ActionDto:
        """ get a ActionDto with a given action name
            return None if there is no with that action name

        Args:
            action_name (str): action name

        Returns:
            ActionDto: ActionDto of the action name
        """
