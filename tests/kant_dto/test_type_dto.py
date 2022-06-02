import unittest
from kant.kant_dto.type_dto import TypeDto


class TestTypeDto(unittest.TestCase):

    def setUp(self):

        self.type_dto = TypeDto("robot")

    def test_type_dto_str(self):
        self.assertEqual("robot", str(self.type_dto))

    def test_type_dto_set_father(self):
        self.type_dto.father = TypeDto("object")
        self.assertEqual("robot - object", str(self.type_dto))

    def test_type_dto_get_name(self):
        self.assertEqual("robot", self.type_dto.name)

    def test_type_dto_eq_true(self):
        type_dto = TypeDto("robot")
        result = (self.type_dto == type_dto)
        self.assertTrue(result)

    def test_type_dto_eq_false_bad_type_name(self):
        type_dto = TypeDto("wp")
        result = (self.type_dto == type_dto)
        self.assertFalse(result)

    def test_type_dto_eq_false_bad_instance(self):
        result = (self.type_dto == 10)
        self.assertFalse(result)
