
from kant.kant_dao import (
    DaoFactoryMethod,
    DaoFamilies
)

from location import Location
from robot import Robot

DaoFactoryMethod(DaoFamilies.MONGO,
                 uri="mongodb://localhost:27017/kant")

# locations
wp1 = Location("wp1", 1.0, 2.5, 0.0, 0.0, 0.0, 0.0, 1.0)
wp1.save()

# robot
rb1 = Robot("rb1")
rb1.robot_at = Location.get("wp1")
rb1.save()

# print
rb1 = Robot.get("rb1")
print(rb1)
