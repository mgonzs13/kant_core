

from kant.kant_dto import *

from domain import *
from location import Location


class Robot:

    def __init__(self, name: str) -> None:

        self.robot_object = ObjectDto(robot, name)
        self.robot_at_fact = None

    def robot_at(self, location: Location) -> None:
        self.robot_at = FactDto(
            robot_at, [self.robot_object, location.location_object])
