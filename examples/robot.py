
from kant.kant_dto import *
from kant.kant_dao import DaoFactoryMethod

from domain import *
from location import Location


class Robot:

    def __init__(self, name: str) -> None:

        self.__robot_object = ObjectDto(robot, name)
        self.__robot_at_fact = None

    def __str__(self) -> str:

        string = "Robot: " + self.name

        if robot_at:
            string += "\n\t" + robot_at.get_name() + ": " + self.robot_at.name

        return string

    @property
    def name(self) -> float:
        return self.__robot_object.get_name()

    @name.setter
    def name(self, name: str) -> None:
        self.__robot_object.set_name(name)

    @property
    def robot_at(self) -> Location:
        return Location.get(self.__robot_at_fact.get_objects()[1].get_name())

    @robot_at.setter
    def robot_at(self, location: Location) -> None:

        dao_factory = DaoFactoryMethod.get_dao_factory()
        object_dao = dao_factory.create_object_dao()

        location_object = object_dao.get(location.name)

        self.__robot_at_fact = FactDto(
            robot_at, [self.__robot_object, location_object])

    # save & get
    def save(self) -> bool:

        dao_factory = DaoFactoryMethod.get_dao_factory()
        object_dao = dao_factory.create_object_dao()

        if not object_dao.save(self.__robot_object):
            return False

        if self.__robot_at_fact:

            fact_dao = dao_factory.create_fact_dao()

            if not fact_dao.save(self.__robot_at_fact):
                return False

        return True

    @staticmethod
    def get(name: str) -> "Robot":
        dao_factory = DaoFactoryMethod.get_dao_factory()
        fact_dao = dao_factory.create_fact_dao()
        object_dao = dao_factory.create_object_dao()

        robot = Robot(name)

        # search for robots facts
        robot_object = object_dao.get(name)

        robot_at_fact = Location._find_fact(
            robot_object, fact_dao.get_by_fluent(robot_at.get_name()))

        if robot_at_fact:
            robot.robot_at = Location.get(
                robot_at_fact.get_objects()[1].get_name())

        return robot
