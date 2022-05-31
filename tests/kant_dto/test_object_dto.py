import unittest
from kant.kant_dto.type_dto import TypeDto
from kant.kant_dto.object_dto import ObjectDto


class TestObjectDto(unittest.TestCase):

    def setUp(self):

        self.type_dto = TypeDto("robot")
        self.object_dto = ObjectDto(self.type_dto, "rb1")

    def test_object_dto_str(self):
        self.assertEqual("rb1 - robot", str(self.object_dto))

    def test_type_dto_get_type(self):
        self.assertEqual("robot", str(self.object_dto.get_type()))

    def test_type_dto_get_name(self):
        self.assertEqual("rb1", self.object_dto.get_name())

    def test_object_dto_eq_true(self):
        object_dto = ObjectDto(self.type_dto, "rb1")
        result = (self.object_dto == object_dto)
        self.assertTrue(result)

    def test_object_dto_eq_false_bad_object_name(self):
        object_dto = ObjectDto(self.type_dto, "rb2")
        result = (self.object_dto == object_dto)
        self.assertFalse(result)

    def test_type_dto_eq_false_bad_instance(self):
        result = (self.object_dto == 10)
        self.assertFalse(result)
