
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

        self.set_fluent(fluent)
        self.set_objects(objects)
        self.set_value(value)
        self.set_is_goal(is_goal)

        Dto.__init__(self)

    def get_fluent(self) -> FluentDto:
        """ fluent getter

        Returns:
            FluentDto: fluent
        """

        return self._fluent

    def set_fluent(self, fluent: FluentDto) -> None:
        """ fluent setter

        Args:
            fluent (FluentDto): fluent
        """

        self._fluent = fluent

    def get_objects(self) -> List[ObjectDto]:
        """ objects list getter

        Returns:
            List[ObjectDto]: list of objects
        """

        return self._objects

    def set_objects(self, objects: List[ObjectDto]) -> None:
        """ objects list setter

        Args:
            objects (List[ObjectDto]): list of objects
        """

        if objects:
            self._objects = objects
        else:
            self._objects = []

    def get_value(self) -> Union[float, bool]:
        """ value getter

        Returns:
            Union[float, bool]: value
        """

        return self._value

    def set_value(self, value: Union[float, bool]) -> None:
        """ value setter

        Args:
            value (Union[float, bool]): value
        """

        if value is None:

            if self.get_fluent().get_is_numeric():
                self._value = 0
            else:
                self._value = True

        else:
            self._value = value

    def get_is_goal(self) -> bool:
        """ is goal getter

        Returns:
            bool: is this fact a goal
        """

        return self._is_goal

    def set_is_goal(self, is_goal: bool) -> None:
        """ is goal setter

        Args:
            is_goal (bool): is this fact a goal
        """

        self._is_goal = is_goal

    def __str__(self) -> str:
        string = "(" + self._fluent.get_name()

        for pddl_object in self._objects:
            string += " " + pddl_object.get_name()

        string += ")"

        if self.get_fluent().get_is_numeric():
            string = "(= " + string + " " + str(self.get_value()) + ")"

        return string

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, FactDto):

            if not other.get_fluent() == self.get_fluent():
                return False

            if not len(other.get_objects()) == len(self.get_objects()):
                return False

            for pddl_object, other_pddl_object in zip(self.get_objects(),
                                                      other.get_objects()):
                if not pddl_object == other_pddl_object:
                    return False

            return True

        return False
