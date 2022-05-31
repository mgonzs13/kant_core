import unittest
from kant.kant_dao.dao_factory import (
    DaoFactoryMethod,
    DaoFamilies
)

from kant.kant_dto import (
    TypeDto,
    ObjectDto,
    FluentDto,
    ConditionEffectDto,
    ActionDto
)


class TestActionDao(unittest.TestCase):

    def setUp(self):
        dao_factory_method = DaoFactoryMethod()
        dao_factory = dao_factory_method.create_dao_factory(
            DaoFamilies.MONGO)

        self.type_dao = dao_factory.create_type_dao()
        self.fluent_dao = dao_factory.create_fluent_dao()
        self.action_dao = dao_factory.create_action_dao()

        self.robot_type = TypeDto("robot", TypeDto("object"))
        self.wp_type = TypeDto("wp")

        self.robot_at = FluentDto(
            "robot_at", [self.robot_type, self.wp_type])
        self.battery_level = FluentDto(
            "battery_level", [self.robot_type], is_numeric=True)

        r = ObjectDto(self.robot_type, "r")
        s = ObjectDto(self.wp_type, "s")
        d = ObjectDto(self.wp_type, "d")

        self.condition_1 = ConditionEffectDto(self.robot_at,
                                              [r, s],
                                              time=ConditionEffectDto.AT_START,
                                              value=True)

        self.condition_2 = ConditionEffectDto(self.battery_level,
                                              [r],
                                              time=ConditionEffectDto.AT_START,
                                              condition_effect=ConditionEffectDto.GREATER,
                                              value=30.00)

        self.effect_1 = ConditionEffectDto(self.robot_at,
                                           [r, s],
                                           time=ConditionEffectDto.AT_START,
                                           value=False)

        self.effect_2 = ConditionEffectDto(self.robot_at,
                                           [r, d],
                                           time=ConditionEffectDto.AT_END,
                                           value=True)

        self.effect_3 = ConditionEffectDto(self.battery_level,
                                           [r],
                                           time=ConditionEffectDto.AT_END,
                                           condition_effect=ConditionEffectDto.DECREASE,
                                           value=10.00)

        self.action_dto = ActionDto(
            "navigation", [r, s, d],
            [self.condition_1, self.condition_2],
            [self.effect_1, self.effect_2, self.effect_3])

    def tearDown(self):
        self.action_dao.delete_all()
        self.fluent_dao.delete_all()
        self.type_dao.delete_all()

    def test_action_dao_save_true(self):
        result = self.action_dao._save(self.action_dto)
        self.assertTrue(result)

    def test_action_dao_save_false_incorrect_condition_types(self):
        self.action_dto.get_conditions(
        )[0].get_objects().reverse()
        result = self.action_dao._save(self.action_dto)
        self.assertFalse(result)

    def test_action_dao_save_false_incorrect_condition_len(self):
        self.action_dto.get_conditions(
        )[0].set_objects([])
        result = self.action_dao._save(self.action_dto)
        self.assertFalse(result)

    def test_action_dao_save_false_durative_condition_no_time(self):
        self.action_dto.get_conditions()[0].set_time("")
        self.action_dto.set_effects([])
        result = self.action_dao._save(self.action_dto)
        self.assertFalse(result)

    def test_action_dao_save_false_durative_effect_no_time(self):
        self.action_dto.get_effects()[1].set_time("")
        self.action_dto.set_conditions([])
        result = self.action_dao._save(self.action_dto)
        self.assertFalse(result)

    def test_action_dao_save_false_no_durative_condition_time(self):
        self.action_dto.set_durative(False)
        self.action_dto.set_effects([])
        result = self.action_dao._save(self.action_dto)
        self.assertFalse(result)

    def test_action_dao_save_false_no_durative_effect_time(self):
        self.action_dto.set_durative(False)
        self.action_dto.set_conditions([])
        result = self.action_dao._save(self.action_dto)
        self.assertFalse(result)

    def test_action_dao_save_false_durative_condition_bad_parameter(self):
        r = ObjectDto(self.robot_type, "a")
        s = ObjectDto(self.wp_type, "s")
        d = ObjectDto(self.wp_type, "d")
        self.action_dto.set_parameters([r, s, d])
        result = self.action_dao._save(self.action_dto)
        self.assertFalse(result)

    def test_action_dao_save_false_durative_effect_bad_parameter(self):
        r = ObjectDto(self.robot_type, "r")
        s = ObjectDto(self.wp_type, "s")
        d = ObjectDto(self.wp_type, "a")
        self.action_dto.set_parameters([r, s, d])
        result = self.action_dao._save(self.action_dto)
        self.assertFalse(result)

    def test_action_dao_save_false_action_already_exist(self):
        result = self.action_dao._save(self.action_dto)
        result = self.action_dao._save(self.action_dto)
        self.assertFalse(result)

    def test_action_dao_get_none(self):
        self.action_dto = self.action_dao.get("navigation")
        self.assertIsNone(self.action_dto)

    def test_action_dao_get(self):
        self.action_dao._save(self.action_dto)

        self.action_dto = self.action_dao.get("navigation")
        self.assertEqual("""\
(:durative-action navigation
\t:parameters ( ?r - robot ?s - wp ?d - wp)
\t:duration (= ?duration 10)
\t:condition (and
\t\t(at start (robot_at ?r ?s))
\t\t(at start (> (battery_level ?r) 30.00))
\t)
\t:effect (and
\t\t(at start (not (robot_at ?r ?s)))
\t\t(at end (robot_at ?r ?d))
\t\t(at end (decrease (battery_level ?r) 10.00))
\t)
)""",
                         str(self.action_dto))

    def test_action_dao_get_all_0(self):
        action_dto_list = self.action_dao.get_all()
        self.assertEqual(0, len(action_dto_list))

    def test_action_dao_update_true(self):
        self.action_dao._save(self.action_dto)
        self.action_dto.get_effects()[0].set_time(
            ConditionEffectDto.AT_END)
        result = self.action_dao._update(self.action_dto)
        self.assertTrue(result)
        self.action_dto = self.action_dao.get("navigation")
        self.assertEqual("""\
(:durative-action navigation
\t:parameters ( ?r - robot ?s - wp ?d - wp)
\t:duration (= ?duration 10)
\t:condition (and
\t\t(at start (robot_at ?r ?s))
\t\t(at start (> (battery_level ?r) 30.00))
\t)
\t:effect (and
\t\t(at end (not (robot_at ?r ?s)))
\t\t(at end (robot_at ?r ?d))
\t\t(at end (decrease (battery_level ?r) 10.00))
\t)
)""",
                         str(self.action_dto))

    def test_action_dao_update_fluent_type_true(self):
        self.action_dao._save(self.action_dto)

        self.action_dto = self.action_dao.get("navigation")
        self.action_dto.get_conditions()[0].get_fluent().set_name("bot_at")
        self.action_dto.get_parameters()[0].get_type().set_name("bot")

        self.assertEqual("""\
(:durative-action navigation
\t:parameters ( ?r - bot ?s - wp ?d - wp)
\t:duration (= ?duration 10)
\t:condition (and
\t\t(at start (bot_at ?r ?s))
\t\t(at start (> (battery_level ?r) 30.00))
\t)
\t:effect (and
\t\t(at start (not (bot_at ?r ?s)))
\t\t(at end (bot_at ?r ?d))
\t\t(at end (decrease (battery_level ?r) 10.00))
\t)
)""",
                         str(self.action_dto))

    def test_action_dao_update_flase(self):
        result = self.action_dao._update(self.action_dto)
        self.assertFalse(result)

    def test_action_dao_save_save_true(self):
        result = self.action_dao.save(self.action_dto)
        self.assertTrue(result)

    def test_action_dao_save_update_true(self):
        result = self.action_dao.save(self.action_dto)
        result = self.action_dao.save(self.action_dto)
        self.assertTrue(result)

    def test_action_dao_normal_action(self):
        self.action_dto.set_durative(False)
        self.condition_1.set_time("")
        self.condition_2.set_time("")
        self.effect_1.set_time("")
        self.effect_2.set_time("")
        self.effect_3.set_time("")

        self.action_dao._save(self.action_dto)
        result = self.action_dao._update(self.action_dto)
        self.assertTrue(result)

        self.action_dto = self.action_dao.get("navigation")
        self.assertEqual("""\
(:action navigation
\t:parameters ( ?r - robot ?s - wp ?d - wp)
\t:precondition (and
\t\t(robot_at ?r ?s)
\t\t(> (battery_level ?r) 30.00)
\t)
\t:effect (and
\t\t(not (robot_at ?r ?s))
\t\t(robot_at ?r ?d)
\t\t(decrease (battery_level ?r) 10.00)
\t)
)""",
                         str(self.action_dto))

    def test_action_dao_delete_false_action_not_exist(self):
        result = self.action_dao.delete(self.action_dto)
        self.assertFalse(result)

    def test_action_dao_delete_true(self):
        self.action_dao.save(self.action_dto)
        result = self.action_dao.delete(self.action_dto)
        self.assertTrue(result)
        self.action_dto = self.action_dao.get("navigation")
        self.assertIsNone(self.action_dto)

    def test_action_dao_delete_all(self):
        self.action_dao.save(self.action_dto)
        result = self.action_dao.delete_all()
        self.assertTrue(result)
        self.action_dto = self.action_dao.get("navigation")
        self.assertIsNone(self.action_dto)
