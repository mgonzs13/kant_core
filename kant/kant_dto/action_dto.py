
""" Action Dto """

from typing import Any, List
from kant.kant_dto.dto import Dto
from kant.kant_dto.condition_effect_dto import ConditionEffectDto
from kant.kant_dto.object_dto import ObjectDto


class ActionDto(Dto):
    """ Action Dto Class """

    def __init__(self, name: str,
                 parameters: List[ObjectDto] = None,
                 conditions: List[ConditionEffectDto] = None,
                 effects: List[ConditionEffectDto] = None,
                 durative: bool = True
                 ) -> None:

        self.set_name(name)
        self.set_parameters(parameters)
        self.set_durative(durative)
        self.set_duration(10)
        self.set_conditions(conditions)
        self.set_effects(effects)

        Dto.__init__(self)

    def get_name(self) -> str:
        """ pdd action name getter

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

    def get_durative(self) -> bool:
        """ durative getter

        Returns:
            bool: is this a durative action
        """

        return self._durative

    def set_durative(self, durative: bool) -> None:
        """ durative setter

        Args:
            durative (bool): is this a durative action
        """

        self._durative = durative

    def get_duration(self) -> int:
        """ duration getter

        Returns:
            int: action duration
        """

        return self._duration

    def set_duration(self, duration: int) -> None:
        """ duration setter

        Args:
            duration (int): action duration
        """

        self._duration = duration

    def get_parameters(self) -> List[ObjectDto]:
        """ parameters list getter

        Returns:
            List[ObjectDto]: list of action parameters
        """

        return self._parameters

    def set_parameters(self, parameters: List[ObjectDto]) -> None:
        """ parameters list setter

        Args:
            parameters (List[ObjectDto]): list of action parameters
        """

        if parameters:
            self._parameters = parameters
        else:
            self._parameters = []

    def get_conditions(self) -> List[ConditionEffectDto]:
        """ conditions list getter

        Returns:
            List[ConditionEffectDto]: list of action conditions
        """

        return self._conditions

    def set_conditions(self, conditions: List[ConditionEffectDto]) -> None:
        """ conditions list setter

        Args:
            conditions (List[ConditionEffectDto]): list of action conditions
        """

        if conditions:
            self._conditions = conditions
        else:
            self._conditions = []

    def get_effects(self) -> List[ConditionEffectDto]:
        """ effects list getter

        Returns:
            List[ConditionEffectDto]: list of action effects
        """
        return self._effects

    def set_effects(self, effects: List[ConditionEffectDto]):
        """ effects list setter

        Args:
            effects (List[ConditionEffectDto]): list of action effects
        """

        if effects:
            self._effects = effects
        else:
            self._effects = []

    def __str__(self) -> str:
        string = "(:"

        # durative
        if self._durative:
            string += "durative-"
        string += "action " + self._name

        # parameters
        string += "\n\t:parameters ("
        for parameter in self._parameters:
            string += " ?" + parameter.get_name() + " - " + \
                parameter.get_type().get_name()
        string += ")"

        # duration
        if self._durative:
            string += "\n\t:duration (= ?duration " + str(self._duration) + ")"

        # conditions
        if self._durative:
            string += "\n\t:condition (and"
        else:
            string += "\n\t:precondition (and"
        for condi in self._conditions:
            string += "\n\t\t" + str(condi)
        string += "\n\t)"

        # effects
        string += "\n\t:effect (and"
        for effect in self._effects:
            string += "\n\t\t" + str(effect)
        string += "\n\t)"

        string += "\n)"

        return string

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ActionDto):
            return self.get_name() == other.get_name()

        return False
