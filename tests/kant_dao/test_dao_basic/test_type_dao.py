import unittest
from kant.kant_dao.dao_factory import (
    DaoFactoryMethod,
    DaoFamilies
)
from kant.kant_dto import TypeDto


class TestTypeDao(unittest.TestCase):

    def setUp(self):
        dao_factory_method = DaoFactoryMethod()
        dao_factory = dao_factory_method.create_dao_factory(
            DaoFamilies.MONGO)

        self.type_dao = dao_factory.create_type_dao()
        self.type_dto = TypeDto("robot", father=TypeDto("object"))

    def tearDown(self):
        self.type_dao.delete_all()

    def test_type_dao_save_true(self):
        result = self.type_dao._save(self.type_dto)
        self.assertTrue(result)

    def test_type_dao_save_false_type_already_exist(self):
        result = self.type_dao._save(self.type_dto)
        result = self.type_dao._save(self.type_dto)
        self.assertFalse(result)

    def test_type_dao_get_none(self):
        self.type_dto = self.type_dao.get("robot")
        self.assertIsNone(self.type_dto)

    def test_type_dao_get(self):
        self.type_dao.save(self.type_dto)
        self.type_dto = self.type_dao.get("robot")
        self.assertEqual("robot - object", str(self.type_dto))

    def test_type_dao_get_all_0(self):
        type_dto_list = self.type_dao.get_all()
        self.assertEqual(0, len(type_dto_list))

    def test_type_dao_update_true(self):
        self.type_dao._save(self.type_dto)
        result = self.type_dao._update(self.type_dto)
        self.assertTrue(result)
        self.type_dto = self.type_dao.get("robot")
        self.assertEqual("robot - object", str(self.type_dto))

    def test_type_dao_update_flase(self):
        result = self.type_dao._update(self.type_dto)
        self.assertFalse(result)

    def test_type_dao_save_save_true(self):
        result = self.type_dao.save(self.type_dto)
        self.assertTrue(result)

    def test_type_dao_save_update_true(self):
        self.type_dao.save(self.type_dto)
        result = self.type_dao.save(self.type_dto)
        self.assertTrue(result)

    def test_type_dao_delete_false_type_not_exist(self):
        result = self.type_dao.delete(self.type_dto)
        self.assertFalse(result)

    def test_type_dao_delete_true(self):
        result = self.type_dao.save(self.type_dto)
        self.assertTrue(result)
        result = self.type_dao.delete(self.type_dto)
        self.assertTrue(result)
        self.type_dto = self.type_dao.get("robot")
        self.assertIsNone(self.type_dto)

    def test_type_dao_delete_all(self):
        self.type_dao.save(self.type_dto)
        result = self.type_dao.delete_all()
        self.assertTrue(result)
        self.assertEqual(0, len(self.type_dao.get_all()))
