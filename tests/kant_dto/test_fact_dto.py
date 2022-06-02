import unittest
from kant.kant_dto.type_dto import TypeDto
from kant.kant_dto.fluent_dto import FluentDto
from kant.kant_dto.fact_dto import FactDto
from kant.kant_dto.object_dto import ObjectDto


class TestFactDto(unittest.TestCase):

    def setUp(self):

        self.robot_type = TypeDto("robot")
        self.wp_type = TypeDto("wp")

        self.robot_at = FluentDto(
            "robot_at", [self.robot_type, self.wp_type])
        self.battery_level = FluentDto(
            "battery_level", [self.robot_type], is_numeric=True)

        self.rb1 = ObjectDto(self.robot_type, "rb1")
        self.wp1 = ObjectDto(self.wp_type, "wp1")

        self.fact_dto = FactDto(
            self.robot_at, [self.rb1, self.wp1])
        self.bat_fact_dto = FactDto(self.battery_level, [self.rb1], value=100)

    def test_fact_dto_str(self):
        self.assertEqual("(robot_at rb1 wp1)",
                         str(self.fact_dto))

    def test_fact_dto_numeric_str(self):
        self.assertEqual("(= (battery_level rb1) 100)",
                         str(self.bat_fact_dto))

    def test_fact_dto_str_no_objects(self):
        self.fact_dto.objects = []
        self.assertEqual("(robot_at)",
                         str(self.fact_dto))

    def test_fact_dto_get_fluent(self):
        self.assertEqual("(robot_at ?r0 - robot ?w1 - wp)",
                         str(self.fact_dto.fluent))

    def test_fact_dto_get_objects(self):
        objects_list = self.fact_dto.objects
        self.assertEqual("rb1", str(objects_list[0].name))
        self.assertEqual("wp1", str(objects_list[1].name))

    def test_fact_dto_get_is_goal(self):
        self.assertFalse(self.fact_dto.is_goal)

    def test_fact_dto_eq_true(self):
        fact_dto = FactDto(
            self.robot_at, [self.rb1, self.wp1])
        result = (self.fact_dto == fact_dto)
        self.assertTrue(result)

    def test_fact_dto_eq_false_bad_objects(self):
        fact_dto = FactDto(
            self.robot_at, [self.wp1, self.rb1])
        result = (self.fact_dto == fact_dto)
        self.assertFalse(result)

    def test_fact_dto_eq_false_bad_len(self):
        fact_dto = FactDto(
            self.robot_at, [self.wp1])
        result = (self.fact_dto == fact_dto)
        self.assertFalse(result)

    def test_fact_dto_eq_false_bad_fluent(self):
        robot_at = FluentDto(
            "robot_on", [self.robot_type, self.wp_type])
        fact_dto = FactDto(
            robot_at, [self.rb1, self.wp1])
        result = (self.fact_dto == fact_dto)
        self.assertFalse(result)

    def test_fact_dto_eq_false_bad_instance(self):
        result = (self.fact_dto == 10)
        self.assertFalse(result)
