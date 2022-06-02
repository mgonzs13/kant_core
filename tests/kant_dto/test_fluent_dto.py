import unittest
from kant.kant_dto.type_dto import TypeDto
from kant.kant_dto.fluent_dto import FluentDto


class TestFluentDto(unittest.TestCase):

    def setUp(self):

        robot_type = TypeDto("robot")
        wp_type = TypeDto("wp")
        self.fluent_dto = FluentDto(
            "robot_at", [robot_type, wp_type])

    def test_fluent_dto_str(self):
        self.assertEqual("(robot_at ?r0 - robot ?w1 - wp)",
                         str(self.fluent_dto))

    def test_fluent_dto_str_no_types(self):
        self.fluent_dto.types = None
        self.assertEqual("(robot_at)",
                         str(self.fluent_dto))

    def test_fluent_dto_get_name(self):
        self.assertEqual("robot_at",
                         self.fluent_dto.name)

    def test_fluent_dto_get_types(self):
        types_list = self.fluent_dto.types
        self.assertEqual(2, len(types_list))
        self.assertEqual("robot", types_list[0].name)
        self.assertEqual("wp", types_list[1].name)

    def test_fluent_dto_eq_true(self):
        fluent_dto = FluentDto("robot_at", [])
        result = (self.fluent_dto == fluent_dto)
        self.assertTrue(result)

    def test_fluent_dto_eq_false_bad_fluent_name(self):
        fluent_dto = FluentDto("robot_on", [])
        result = (self.fluent_dto == fluent_dto)
        self.assertFalse(result)

    def test_fluent_dto_eq_false_bad_instance(self):
        result = (self.fluent_dto == 10)
        self.assertFalse(result)
