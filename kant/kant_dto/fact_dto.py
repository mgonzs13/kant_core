
""" Fact Dto """

from typing import List, Union, Any
from kant.kant_dto.dto import Dto
from kant.kant_dto.fluent_dto import FluentDto
from kant.kant_dto.object_dto import ObjectDto


class FactDto(Dto):
    """ Fact Dto Class """

    def __init__(self,
                 fluent: FluentDto,
                 objects: List[ObjectDto] = None,
                 value: Union[float, bool] = None,
                 is_goal: bool = False
                 ) -> None:

        self.fluent = fluent
        self.objects = objects
        self.value = value
        self.is_goal = is_goal

        Dto.__init__(self)

    @property
    def fluent(self) -> FluentDto:
        return self._fluent

    @fluent.setter
    def fluent(self, fluent: FluentDto) -> None:
        self._fluent = fluent

    @property
    def objects(self) -> List[ObjectDto]:
        return self._objects

    @objects.setter
    def objects(self, objects: List[ObjectDto]) -> None:

        if objects:
            self._objects = objects
        else:
            self._objects = []

    @property
    def value(self) -> Union[float, bool]:
        return self._value

    @value.setter
    def value(self, value: Union[float, bool]) -> None:

        if value is None:

            if self.fluent.is_numeric:
                self._value = 0
            else:
                self._value = True

        else:
            self._value = value

    @property
    def is_goal(self) -> bool:
        return self._is_goal

    @is_goal.setter
    def is_goal(self, is_goal: bool) -> None:
        self._is_goal = is_goal

    def to_pddl(self) -> str:
        string = "(" + self.fluent.name

        for object in self._objects:
            string += " " + object.name

        string += ")"

        if self.fluent.is_numeric:
            string = "(= " + string + " " + str(self.value) + ")"

        return string

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, FactDto):

            if not other.fluent == self.fluent:
                return False

            if not len(other.objects) == len(self.objects):
                return False

            for object, other_object in zip(self.objects,
                                            other.objects):
                if not object == other_object:
                    return False

            return True

        return False
