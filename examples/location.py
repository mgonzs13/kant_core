
from typing import List
from kant.kant_dao import DaoFactoryMethod

from kant.kant_dto import *


# domain
location = TypeDto("location")

pose_x = FluentDto("pose_x", [location], is_numeric=True)
pose_y = FluentDto("pose_y", [location], is_numeric=True)
pose_z = FluentDto("pose_z", [location], is_numeric=True)

quaternion_x = FluentDto("quaternion_x", [location], is_numeric=True)
quaternion_y = FluentDto("quaternion_y", [location], is_numeric=True)
quaternion_z = FluentDto("quaternion_z", [location], is_numeric=True)
quaternion_w = FluentDto("quaternion_w", [location], is_numeric=True)


class Location:

    def __init__(self,
                 name: str,
                 p_x: float = 0.0,
                 p_y: float = 0.0,
                 p_z: float = 0.0,
                 q_x: float = 0.0,
                 q_y: float = 0.0,
                 q_z: float = 0.0,
                 q_w: float = 1.0
                 ) -> None:

        self._location_object = ObjectDto(location, name)

        self._pose_x_fact = FactDto(
            pose_x, [self._location_object], value=p_x)
        self._pose_y_fact = FactDto(
            pose_y, [self._location_object], value=p_y)
        self._pose_z_fact = FactDto(
            pose_z, [self._location_object], value=p_z)

        self._quaternion_x_fact = FactDto(
            quaternion_x, [self._location_object], value=q_x)
        self._quaternion_y_fact = FactDto(
            quaternion_y, [self._location_object], value=q_y)
        self._quaternion_z_fact = FactDto(
            quaternion_z, [self._location_object], value=q_z)
        self._quaternion_w_fact = FactDto(
            quaternion_w, [self._location_object], value=q_w)

        self._fact_list = [self._pose_x_fact, self._pose_y_fact, self._pose_z_fact,
                           self._quaternion_x_fact, self._quaternion_y_fact,
                           self._quaternion_z_fact, self._quaternion_w_fact]

        self.save()

    def __str__(self) -> str:

        string = "Location: " + self._location_object.get_name() + "\n"

        for fact_dto in self._fact_list:
            string += "\t" + fact_dto.get_fluent().get_name() + ": " + \
                str(fact_dto.get_value()) + "\n"

        return string

    @property
    def name(self) -> float:
        return self._location_object.get_name()

    @name.setter
    def name(self, name: str) -> None:
        self._location_object.set_name(name)
        self.save()

    # pose
    @property
    def pose_x(self) -> float:
        return self._pose_x_fact.get_value()

    @pose_x.setter
    def pose_x(self, value: float) -> None:
        self._pose_x_fact.set_value(value)
        self.save()

    @property
    def pose_y(self) -> float:
        return self._pose_y_fact.get_value()

    @pose_y.setter
    def pose_y(self, value: float) -> None:
        self._pose_y_fact.set_value(value)
        self.save()

    @property
    def pose_z(self) -> float:
        return self._pose_z_fact.get_value()

    @pose_z.setter
    def pose_z(self, value: float) -> None:
        self._pose_z_fact.set_value(value)
        self.save()

    # quaternion
    @property
    def quaternion_x(self) -> float:
        return self._quaternion_x_fact.get_value()

    @quaternion_x.setter
    def quaternion_x(self, value: float) -> None:
        self._quaternion_x_fact.set_value(value)
        self.save()

    @property
    def quaternion_y(self) -> float:
        return self._quaternion_y_fact.get_value()

    @quaternion_y.setter
    def quaternion_y(self, value: float) -> None:
        self._quaternion_y_fact.set_value(value)
        self.save()

    @property
    def quaternion_z(self) -> float:
        return self._quaternion_z_fact.get_value()

    @quaternion_z.setter
    def quaternion_z(self, value: float) -> None:
        self._quaternion_z_fact.set_value(value)
        self.save()

    @property
    def quaternion_w(self) -> float:
        return self._quaternion_w_fact.get_value()

    @quaternion_w.setter
    def quaternion_w(self, value: float) -> None:
        self._quaternion_w_fact.set_value(value)
        self.save()

    # save & get
    def save(self) -> bool:

        dao_factory = DaoFactoryMethod.get_dao_factory()
        fact_dao = dao_factory.create_fact_dao()

        for fact_dto in self._fact_list:
            if not fact_dao.save(fact_dto):
                return False

    @staticmethod
    def get(name: str) -> "Location":
        dao_factory = DaoFactoryMethod.get_dao_factory()
        fact_dao = dao_factory.create_fact_dao()
        object_dao = dao_factory.create_object_dao()

        location = object_dao.get(name)

        p_x = Location._find_fact(
            location, fact_dao.get_by_fluent(pose_x.get_name())).get_value()
        p_y = Location._find_fact(
            location, fact_dao.get_by_fluent(pose_y.get_name())).get_value()
        p_z = Location._find_fact(
            location, fact_dao.get_by_fluent(pose_z.get_name())).get_value()

        q_x = Location._find_fact(
            location, fact_dao.get_by_fluent(quaternion_x.get_name())).get_value()
        q_y = Location._find_fact(
            location, fact_dao.get_by_fluent(quaternion_y.get_name())).get_value()
        q_z = Location._find_fact(
            location, fact_dao.get_by_fluent(quaternion_z.get_name())).get_value()
        q_w = Location._find_fact(
            location, fact_dao.get_by_fluent(quaternion_w.get_name())).get_value()

        if (p_x is None or p_y is None or p_z is None or
                q_x is None or q_y is None or q_z is None or q_w is None):
            return None

        return Location(name,
                        p_x, p_y, p_z,
                        q_x, q_y, q_z, q_w)

    @staticmethod
    def _find_fact(object_dto: ObjectDto, fact_list: List[FactDto]) -> FactDto:

        for fact_dto in fact_list:

            if object_dto in fact_dto.get_objects():
                return fact_dto

        return None
