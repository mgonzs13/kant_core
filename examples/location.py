
from typing import List

from kant.kant_dto import *
from kant.kant_dao import DaoFactory

from domain import *


class Location:

    def __init__(self,
                 name: str,
                 p_x: float,
                 p_y: float,
                 p_z: float,
                 q_x: float,
                 q_y: float,
                 q_z: float,
                 q_w: float
                 ) -> None:

        self.location_object = ObjectDto(location, name)

        self.pose_x_fact = FactDto(
            pose_x, [self.location_object], value=p_x)
        self.pose_y_fact = FactDto(
            pose_y, [self.location_object], value=p_y)
        self.pose_z_fact = FactDto(
            pose_z, [self.location_object], value=p_z)

        self.quaternion_x_fact = FactDto(
            quaternion_x, [self.location_object], value=q_x)
        self.quaternion_y_fact = FactDto(
            quaternion_y, [self.location_object], value=q_y)
        self.quaternion_z_fact = FactDto(
            quaternion_z, [self.location_object], value=q_z)
        self.quaternion_w_fact = FactDto(
            quaternion_w, [self.location_object], value=q_w)

        self.fact_list = [self.pose_x_fact, self.pose_y_fact, self.pose_z_fact,
                          self.quaternion_x_fact, self.quaternion_y_fact,
                          self.quaternion_z_fact, self.quaternion_w_fact]

    def save(self, dao_factory: DaoFactory) -> bool:

        fact_dao = dao_factory.create_fact_dao()

        for fact_dto in self.fact_list:
            if not fact_dao.save(fact_dto):
                return False

    def __str__(self) -> str:

        string = "Location: " + self.location_object.get_name() + "\n"

        for fact_dto in self.fact_list:
            string += "\t" + fact_dto.get_fluent().get_name() + ": " + \
                str(fact_dto.get_value()) + "\n"

        return string

    @staticmethod
    def get(name: str, dao_factory: DaoFactory) -> "Location":
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

        return Location(name,
                        p_x, p_y, p_z,
                        q_x, q_y, q_z, q_w)

    @staticmethod
    def _find_fact(object_dto: ObjectDto, fact_list: List[FactDto]) -> FactDto:

        for fact_dto in fact_list:

            if object_dto in fact_dto.get_objects():
                return fact_dto

        return None
