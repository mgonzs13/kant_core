import unittest
from kant.kant_dao.dao_factory import (
    DaoFactoryMethod,
    DaoFamilies
)
from kant.kant_dto import (
    TypeDto,
    ObjectDto
)


class TestObjectDao(unittest.TestCase):

    def setUp(self):
        dao_factory_method = DaoFactoryMethod()
        dao_factory = dao_factory_method.create_dao_factory(
            DaoFamilies.MONGO)

        self.object_dao = dao_factory.create_object_dao()

        type_dto = TypeDto("robot", father=TypeDto("object"))
        self.object_dto = ObjectDto(type_dto, "rb1")

    def tearDown(self):
        self.object_dao.delete_all()

    def test_object_dao_save_true(self):
        result = self.object_dao._save(self.object_dto)
        self.assertTrue(result)

    def test_object_dao_save_false_object_already_exist(self):
        result = self.object_dao._save(self.object_dto)
        result = self.object_dao._save(self.object_dto)
        self.assertFalse(result)

    def test_object_dao_get_none(self):
        self.object_dto = self.object_dao.get("rb1")
        self.assertIsNone(self.object_dto)

    def test_object_dao_get(self):
        self.object_dao._save(self.object_dto)
        self.object_dto = self.object_dao.get("rb1")
        self.assertEqual("rb1 - robot", str(self.object_dto))

    def test_object_dao_get_all_0(self):
        object_dto_list = self.object_dao.get_all()
        self.assertEqual(0, len(object_dto_list))

    def test_object_dao_update_true(self):
        self.object_dao._save(self.object_dto)
        result = self.object_dao._update(self.object_dto)
        self.assertTrue(result)
        self.object_dto = self.object_dao.get("rb1")
        self.assertEqual("rb1 - robot", str(self.object_dto))

    def test_object_dao_update_flase(self):
        result = self.object_dao._update(self.object_dto)
        self.assertFalse(result)

    def test_object_dao_save_save_true(self):
        result = self.object_dao.save(self.object_dto)
        self.assertTrue(result)

    def test_object_dao_save_true(self):
        self.object_dao._save(self.object_dto)
        result = self.object_dao.save(self.object_dto)
        self.assertTrue(result)

    def test_object_dao_delete_false_object_not_exist(self):
        result = self.object_dao.delete(self.object_dto)
        self.assertFalse(result)

    def test_object_dao_delete_true(self):
        self.object_dao.save(self.object_dto)
        result = self.object_dao.delete(self.object_dto)
        self.assertTrue(result)

    def test_object_dao_delete_all(self):
        self.object_dao.save(self.object_dto)
        result = self.object_dao.delete_all()
        self.assertTrue(result)
        self.assertEqual(0, len(self.object_dao.get_all()))
