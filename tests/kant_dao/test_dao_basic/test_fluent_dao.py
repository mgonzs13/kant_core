import unittest
from kant.kant_dao import DaoFactoryMethod
from kant.kant_dto import (
    TypeDto,
    FluentDto
)


class TestPredicateDao(unittest.TestCase):

    def setUp(self):
        dao_factory = DaoFactoryMethod.get_dao_factory()

        self.type_dao = dao_factory.create_type_dao()
        self.fluent_dao = dao_factory.create_fluent_dao()

        robot_type = TypeDto("robot", father=TypeDto("object"))
        wp_type = TypeDto("wp")

        self.fluent_dto = FluentDto(
            "robot_at", [robot_type, wp_type])
        self.battery_level = FluentDto(
            "battery_level", [robot_type], is_numeric=True)

    def tearDown(self):
        self.fluent_dao.delete_all()
        self.type_dao.delete_all()

    def test_fluent_dao_save_true(self):
        result = self.fluent_dao._save(self.fluent_dto)
        self.assertTrue(result)
        self.assertEqual(1, len(self.fluent_dao.get_all()))
        self.assertEqual("(robot_at ?r0 - robot ?w1 - wp)", str(
            self.fluent_dao.get("robot_at")))

    def test_fluent_dao_numeric_save_true(self):
        result = self.fluent_dao._save(self.battery_level)
        self.assertTrue(result)
        self.assertEqual(1, len(self.fluent_dao.get_all()))
        self.assertEqual("(battery_level ?r0 - robot)",
                         str(self.fluent_dao.get("battery_level")))
        self.assertTrue(self.fluent_dao.get("battery_level").get_is_numeric())

    def test_fluent_dao_save_true_no_types(self):
        self.fluent_dto = FluentDto("robot_at")
        result = self.fluent_dao._save(self.fluent_dto)
        self.assertTrue(result)
        self.assertEqual(1, len(self.fluent_dao.get_all()))

    def test_fluent_dao_save_false_fluent_already_exist(self):
        result = self.fluent_dao._save(self.fluent_dto)
        result = self.fluent_dao._save(self.fluent_dto)
        self.assertFalse(result)

    def test_fluent_dao_get_none(self):
        self.fluent_dto = self.fluent_dao.get("robot_at")
        self.assertIsNone(self.fluent_dto)

    def test_fluent_dao_get(self):
        self.fluent_dao._save(self.fluent_dto)
        self.fluent_dto = self.fluent_dao.get("robot_at")
        self.assertEqual("(robot_at ?r0 - robot ?w1 - wp)",
                         str(self.fluent_dto))

    def test_fluent_dao_get_all_0(self):
        fluent_dto_list = self.fluent_dao.get_all()
        self.assertEqual(0, len(fluent_dto_list))

    def test_fluent_dao_update_true(self):
        self.fluent_dao._save(self.fluent_dto)
        result = self.fluent_dao._update(self.fluent_dto)
        self.assertTrue(result)
        self.fluent_dto = self.fluent_dao.get("robot_at")
        self.assertEqual("(robot_at ?r0 - robot ?w1 - wp)",
                         str(self.fluent_dto))

    def test_fluent_dao_update_flase(self):
        result = self.fluent_dao._update(self.fluent_dto)
        self.assertFalse(result)

    def test_fluent_dao_save_save_true(self):
        result = self.fluent_dao.save(self.fluent_dto)
        self.assertTrue(result)

    def test_fluent_dao_save_update_true(self):
        self.fluent_dao._save(self.fluent_dto)
        result = self.fluent_dao.save(self.fluent_dto)
        self.assertTrue(result)

    def test_fluent_dao_delete_false_fluent_not_exist(self):
        result = self.fluent_dao.delete(self.fluent_dto)
        self.assertFalse(result)

    def test_fluent_dao_delete_true(self):
        self.fluent_dao.save(self.fluent_dto)
        result = self.fluent_dao.delete(self.fluent_dto)
        self.assertTrue(result)
        self.fluent_dto = self.fluent_dao.get("robot_at")
        self.assertIsNone(self.fluent_dto)

    def test_fluent_dao_delete_all(self):
        self.fluent_dao.save(self.fluent_dto)
        result = self.fluent_dao.delete_all()
        self.assertTrue(result)
        self.assertEqual(0, len(self.fluent_dao.get_all()))
