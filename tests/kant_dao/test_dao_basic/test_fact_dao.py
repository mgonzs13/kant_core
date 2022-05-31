import unittest
from kant.kant_dao import DaoFactoryMethod
from kant.kant_dto import (
    TypeDto,
    ObjectDto,
    FluentDto,
    FactDto,
)


class TestFactDao(unittest.TestCase):

    def setUp(self):
        dao_factory = DaoFactoryMethod.get_dao_factory()

        self.type_dao = dao_factory.create_type_dao()
        self.object_dao = dao_factory.create_object_dao()
        self.fluent_dao = dao_factory.create_fluent_dao()
        self.fact_dao = dao_factory.create_fact_dao()

        self.robot_type = TypeDto("robot", father=TypeDto("object"))
        self.wp_type = TypeDto("wp")

        self.robot_at = FluentDto(
            "robot_at", [self.robot_type, self.wp_type])
        self.battery_level = FluentDto(
            "battery_level", [self.robot_type], is_numeric=True)

        self.rb1 = ObjectDto(self.robot_type, "rb1")
        self.wp1 = ObjectDto(self.wp_type, "wp1")

        self.fact_dto = FactDto(
            self.robot_at, [self.rb1, self.wp1])
        self.bat_fact_dto = FactDto(
            self.battery_level, [self.rb1], value=100)

    def tearDown(self):
        self.fact_dao.delete_all()
        self.object_dao.delete_all()
        self.fluent_dao.delete_all()
        self.type_dao.delete_all()

    def test_fact_dao_save_true(self):
        result = self.fact_dao._save(self.fact_dto)
        self.assertTrue(result)
        self.assertEqual(1, len(self.fact_dao.get_propositions()))
        self.assertEqual(0, len(self.fact_dao.get_functions()))

    def test_fact_dao_numeric_save_true(self):
        result = self.fact_dao._save(self.bat_fact_dto)
        self.assertTrue(result)
        self.assertEqual(0, len(self.fact_dao.get_propositions()))
        self.assertEqual(1, len(self.fact_dao.get_functions()))
        self.assertEqual("(= (battery_level rb1) 100.00)",
                         str(self.fact_dao.get_functions()[0]))

    def test_fact_dao_save_true_no_objects(self):
        self.robot_at = FluentDto("robot_at")
        self.fact_dto = FactDto(self.robot_at)
        result = self.fact_dao._save(self.fact_dto)
        self.assertTrue(result)
        self.assertEqual(1, len(self.fact_dao.get_all()))

    def test_fact_dao_save_false_incorrect_fact_types(self):
        self.fact_dto.get_objects().reverse()
        result = self.fact_dao._save(self.fact_dto)
        self.assertFalse(result)

    def test_fact_dao_save_false_incorrect_fact_len(self):
        self.fact_dto.set_objects([])
        result = self.fact_dao._save(self.fact_dto)
        self.assertFalse(result)

    def test_fact_dao_save_false_fact_already_exist(self):
        result = self.fact_dao._save(self.fact_dto)
        result = self.fact_dao._save(self.fact_dto)
        self.assertFalse(result)

    def test_fact_dao_get_by_fluent_empty(self):
        self.fact_dto = self.fact_dao.get_by_fluent(
            "robot_at")
        self.assertEqual([], self.fact_dto)

    def test_fact_dao_get_by_fluent(self):
        self.fact_dao._save(self.fact_dto)

        self.fact_dto = self.fact_dao.get_by_fluent("robot_at")[
            0]
        self.assertEqual("(robot_at rb1 wp1)",
                         str(self.fact_dto))

    def test_fact_dao_get_goals(self):
        self.fact_dto.set_is_goal(True)
        self.fact_dao._save(self.fact_dto)
        self.fact_dto = self.fact_dao.get_goals()[0]
        self.assertEqual("(robot_at rb1 wp1)",
                         str(self.fact_dto))

    def test_fact_dao_get_goals_empty(self):
        self.fact_dto.set_is_goal(False)
        self.fact_dao._save(self.fact_dto)
        self.fact_dto = self.fact_dao.get_goals()
        self.assertEqual(0, len(self.fact_dto))

    def test_fact_dao_get_no_goals(self):
        self.fact_dao._save(self.fact_dto)
        self.fact_dto = self.fact_dao.get_no_goals()[0]
        self.assertEqual("(robot_at rb1 wp1)",
                         str(self.fact_dto))

    def test_fact_dao_get_no_goals_empty(self):
        self.fact_dto.set_is_goal(True)
        self.fact_dao._save(self.fact_dto)
        self.fact_dto = self.fact_dao.get_no_goals()
        self.assertEqual(0, len(self.fact_dto))

    def test_fact_dao_get_all_0(self):
        fact_dto_list = self.fact_dao.get_all()
        self.assertEqual(0, len(fact_dto_list))

    def test_fact_dao_update_true(self):
        self.fact_dao._save(self.fact_dto)
        result = self.fact_dao._update(self.fact_dto)
        self.assertTrue(result)
        self.fact_dto = self.fact_dao.get_by_fluent("robot_at")[
            0]
        self.assertEqual("(robot_at rb1 wp1)",
                         str(self.fact_dto))

    def test_fact_dao_update_flase_fact_not_exists(self):
        result = self.fact_dao._update(self.fact_dto)
        self.assertFalse(result)

    def test_fact_dao_update_false_incorrect_fact_types(self):
        self.fact_dto.get_objects().reverse()
        result = self.fact_dao._update(self.fact_dto)
        self.assertFalse(result)

    def test_fact_dao_save_save_true(self):
        result = self.fact_dao.save(self.fact_dto)
        self.assertTrue(result)

    def test_fact_dao_save_update_true(self):
        result = self.fact_dao.save(self.fact_dto)
        result = self.fact_dao.save(self.fact_dto)
        self.assertTrue(result)

    def test_fact_dao_delete_false_fact_not_exist(self):
        result = self.fact_dao.delete(self.fact_dto)
        self.assertFalse(result)

    def test_fact_dao_delete_true(self):
        self.fact_dao.save(self.fact_dto)
        result = self.fact_dao.delete(self.fact_dto)
        self.assertTrue(result)
        self.fact_dto = self.fact_dao.get_by_fluent(
            "robot_at")
        self.assertEqual(0, len(self.fact_dto))

    def test_fact_dao_delete_all(self):
        self.fact_dao.save(self.fact_dto)
        result = self.fact_dao.delete_all()
        self.assertTrue(result)
        self.fact_dto = self.fact_dao.get_by_fluent(
            "robot_at")
        self.assertEqual(0, len(self.fact_dto))

    def test_fact_dao_modify_type(self):
        self.fact_dao.save(self.fact_dto)
        self.fact_dto = self.fact_dao.get_by_fluent("robot_at")[0]
        self.fact_dto.get_fluent().get_types()[0].set_name("bot")
        self.assertEqual("rb1 - bot", str(self.fact_dto.get_objects()[0]))
