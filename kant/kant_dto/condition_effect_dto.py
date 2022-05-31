
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

        self.set_time(time)
        self.set_condition_effect(condition_effect)

        super().__init__(fluent_dto, objects_list, value)

    def get_time(self) -> str:
        """ time getter

        Returns:
            str: time the condition/effect will be resolved
        """

        return self._time

    def set_time(self, time: str) -> None:
        """ time setter

        Args:
            time (str): time the condition/effect will be resolved
        """

        self._time = time

    def get_condition_effect(self) -> str:
        """ condition/effect getter

        Returns:
            str: condition or effect
        """

        return self._condition_effect

    def set_condition_effect(self, condition_effect: str) -> None:
        """ condition/effect setter

        Args:
            condition_effect (str): condition or effect
        """

        if condition_effect is None:
            self._condition_effect = ConditionEffectDto.ASSIGN

        else:
            self._condition_effect = condition_effect

        self._condition_effect = condition_effect

    def __str__(self) -> str:

        string = "(" + self.get_fluent().get_name()

        for object in self.get_objects():
            string += " ?" + object.get_name()

        string += ")"

        if self.get_fluent().get_is_numeric():
            string = "(" + self.get_condition_effect() + " " + \
                string + " " + str(self.get_value()) + ")"

        else:
            if not self.get_value():
                string = "(not " + string + ")"

        if self._time:
            string = "(" + self._time + " " + string + ")"

        return string

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ConditionEffectDto):

            if not other.get_fluent() == self.get_fluent():
                return False

            if not len(other.get_objects()) == len(self.get_objects()):
                return False

            if not other.get_value() == self.get_value():
                return False

            if not other.get_time() == self.get_time():
                return False

            for object, other_object in zip(self.get_objects(),
                                            other.get_objects()):
                if not object == other_object:
                    return False

            return True

        return False
