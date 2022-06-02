
from kant.kant_dto import *
from kant.kant_dao import DaoFactoryMethod

from location import Location
from world_object import WorldObject, world_object, at

# domain
robot = TypeDto("robot", father=world_object)


class Robot(WorldObject):

    def __init__(self, name: str) -> None:

        super().__init__(name, save=False)
        self._world_object_object = ObjectDto(robot, name)
        self.save()

    # save & get
    def save(self) -> bool:
        res = super().save()
        return res

    @staticmethod
    def get(name: str) -> "Robot":
        dao_factory = DaoFactoryMethod.get_dao_factory()
        fact_dao = dao_factory.create_fact_dao()
        object_dao = dao_factory.create_object_dao()

        robot = Robot(name)

        # search for robots facts
        robot_object = object_dao.get(name)

        at_fact = Location._find_fact(
            robot_object, fact_dao.get_by_fluent(at.name))

        if at_fact:
            robot.at = Location.get(
                at_fact.objects[1].name)

        return robot
