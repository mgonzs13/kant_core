
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

        self.name = name
        self.parameters = parameters
        self.durative = durative
        self.duration = 10
        self.conditions = conditions
        self.effects = effects

        Dto.__init__(self)

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name

    @property
    def durative(self) -> bool:
        return self._durative

    @durative.setter
    def durative(self, durative: bool) -> None:
        self._durative = durative

    @property
    def duration(self) -> int:
        return self._duration

    @duration.setter
    def duration(self, duration: int) -> None:
        self._duration = duration

    @property
    def parameters(self) -> List[ObjectDto]:
        return self._parameters

    @parameters.setter
    def parameters(self, parameters: List[ObjectDto]) -> None:

        if parameters:
            self._parameters = parameters
        else:
            self._parameters = []

    @property
    def conditions(self) -> List[ConditionEffectDto]:
        return self._conditions

    @conditions.setter
    def conditions(self, conditions: List[ConditionEffectDto]) -> None:

        if conditions:
            self._conditions = conditions
        else:
            self._conditions = []

    @property
    def effects(self) -> List[ConditionEffectDto]:
        return self._effects

    @effects.setter
    def effects(self, effects: List[ConditionEffectDto]):

        if effects:
            self._effects = effects
        else:
            self._effects = []

    def to_pddl(self) -> str:
        string = "(:"

        # durative
        if self.durative:
            string += "durative-"
        string += "action " + self.name

        # parameters
        string += "\n\t:parameters ("
        for parameter in self.parameters:
            string += " ?" + parameter.name + " - " + \
                parameter.type.name
        string += ")"

        # duration
        if self.durative:
            string += "\n\t:duration (= ?duration " + str(self.duration) + ")"

        # conditions
        if self.durative:
            string += "\n\t:condition (and"
        else:
            string += "\n\t:precondition (and"
        for condi in self.conditions:
            string += "\n\t\t" + str(condi)
        string += "\n\t)"

        # effects
        string += "\n\t:effect (and"
        for effect in self.effects:
            string += "\n\t\t" + str(effect)
        string += "\n\t)"

        string += "\n)"

        return string

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ActionDto):
            return self.name == other.name

        return False
