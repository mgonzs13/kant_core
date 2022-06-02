
""" Condition/Effect Dto """

from typing import Any, List, Union
from kant.kant_dto.fact_dto import FactDto
from kant.kant_dto.fluent_dto import FluentDto
from kant.kant_dto.object_dto import ObjectDto


class ConditionEffectDto(FactDto):
    """ Condition/Effect Class Dto """

    # times
    AT_START: str = "at start"
    AT_END: str = "at end"
    OVER_ALL: str = "over all"

    # conditions
    GREATER: str = ">"
    LOWER: str = "<"
    EQUALS: str = "="

    # effects
    INCREASE: str = "increase"
    DECREASE: str = "decrease"
    ASSIGN: str = "assign"

    def __init__(self,
                 fluent_dto: FluentDto,
                 objects_list: List[ObjectDto] = None,
                 value: Union[float, bool] = None,
                 time: str = None,
                 condition_effect: str = None
                 ) -> None:

        self.time = time
        self.condition_effect = condition_effect

        super().__init__(fluent_dto, objects_list, value)

    @property
    def time(self) -> str:
        return self._time

    @time.setter
    def time(self, time: str) -> None:
        self._time = time

    @property
    def condition_effect(self) -> str:
        return self._condition_effect

    @condition_effect.setter
    def condition_effect(self, condition_effect: str) -> None:

        if condition_effect is None:
            self._condition_effect = ConditionEffectDto.ASSIGN

        else:
            self._condition_effect = condition_effect

        self._condition_effect = condition_effect

    def to_pddl(self) -> str:

        string = "(" + self.fluent.name

        for object in self.objects:
            string += " ?" + object.name

        string += ")"

        if self.fluent.is_numeric:
            string = "(" + self.condition_effect + " " + \
                string + " " + str(self.value) + ")"

        else:
            if not self.value:
                string = "(not " + string + ")"

        if self._time:
            string = "(" + self._time + " " + string + ")"

        return string

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ConditionEffectDto):

            if not other.fluent == self.fluent:
                return False

            if not len(other.objects) == len(self.objects):
                return False

            if not other.value == self.value:
                return False

            if not other.time == self.time:
                return False

            for object, other_object in zip(self.objects,
                                            other.objects):
                if not object == other_object:
                    return False

            return True

        return False
