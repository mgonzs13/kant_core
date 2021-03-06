import unittest
from kant.kant_dao import DaoFactoryMethod
from kant.kant_dto import (
    TypeDto,
    ObjectDto,
    FluentDto,
    ConditionEffectDto,
    ActionDto
)


class TestActionDao(unittest.TestCase):

    def setUp(self):
        dao_factory = DaoFactoryMethod.get_dao_factory()

        self.type_dao = dao_factory.create_type_dao()
        self.fluent_dao = dao_factory.create_fluent_dao()
        self.action_dao = dao_factory.create_action_dao()

        self.object_type = TypeDto("object")
        self.robot_type = TypeDto("robot", TypeDto("object"))
        self.wp_type = TypeDto("wp")

        self.at = FluentDto(
            "at", [self.object_type, self.wp_type])
        self.battery_level = FluentDto(
            "battery_level", [self.robot_type], is_numeric=True)

        r = ObjectDto(self.robot_type, "r")
        s = ObjectDto(self.wp_type, "s")
        d = ObjectDto(self.wp_type, "d")

        self.condition_1 = ConditionEffectDto(self.at,
                                              [r, s],
                                              time=ConditionEffectDto.AT_START,
                                              value=True)

        self.condition_2 = ConditionEffectDto(self.battery_level,
                                              [r],
                                              time=ConditionEffectDto.AT_START,
                                              condition_effect=ConditionEffectDto.GREATER,
                                              value=30.00)

        self.effect_1 = ConditionEffectDto(self.at,
                                           [r, s],
                                           time=ConditionEffectDto.AT_START,
                                           value=False)

        self.effect_2 = ConditionEffectDto(self.at,
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
        self.fluent_dao.delete_all()
        self.action_dao.delete_all()
        self.type_dao.delete_all()

    def test_action_dao_save_true(self):
        result = self.action_dao._save(self.action_dto)
        self.assertTrue(result)

    def test_action_dao_save_false_incorrect_condition_types(self):
        self.action_dto.conditions[0].objects.reverse()
        result = self.action_dao._save(self.action_dto)
        self.assertFalse(result)

    def test_action_dao_save_false_incorrect_condition_len(self):
        self.action_dto.conditions[0].objects = []
        result = self.action_dao._save(self.action_dto)
        self.assertFalse(result)

    def test_action_dao_save_false_durative_condition_no_time(self):
        self.action_dto.conditions[0].time = ""
        self.action_dto.effects = []
        result = self.action_dao._save(self.action_dto)
        self.assertFalse(result)

    def test_action_dao_save_false_durative_effect_no_time(self):
        self.action_dto.effects[1].time = ""
        self.action_dto.conditions = []
        result = self.action_dao._save(self.action_dto)
        self.assertFalse(result)

    def test_action_dao_save_false_no_durative_condition_time(self):
        self.action_dto.durative = False
        self.action_dto.effects = []
        result = self.action_dao._save(self.action_dto)
        self.assertFalse(result)

    def test_action_dao_save_false_no_durative_effect_time(self):
        self.action_dto.durative = False
        self.action_dto.conditions = []
        result = self.action_dao._save(self.action_dto)
        self.assertFalse(result)

    def test_action_dao_save_false_durative_condition_bad_parameter(self):
        r = ObjectDto(self.robot_type, "a")
        s = ObjectDto(self.wp_type, "s")
        d = ObjectDto(self.wp_type, "d")
        self.action_dto.parameters = [r, s, d]
        result = self.action_dao._save(self.action_dto)
        self.assertFalse(result)

    def test_action_dao_save_false_durative_effect_bad_parameter(self):
        r = ObjectDto(self.robot_type, "r")
        s = ObjectDto(self.wp_type, "s")
        d = ObjectDto(self.wp_type, "a")
        self.action_dto.parameters = [r, s, d]
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
\t\t(at start (at ?r ?s))
\t\t(at start (> (battery_level ?r) 30.00))
\t)
\t:effect (and
\t\t(at start (not (at ?r ?s)))
\t\t(at end (at ?r ?d))
\t\t(at end (decrease (battery_level ?r) 10.00))
\t)
)""",
                         str(self.action_dto))

    def test_action_dao_get_all_0(self):
        action_dto_list = self.action_dao.get_all()
        self.assertEqual(0, len(action_dto_list))

    def test_action_dao_update_true(self):
        self.action_dao._save(self.action_dto)
        self.action_dto.effects[0].time = ConditionEffectDto.AT_END
        result = self.action_dao._update(self.action_dto)
        self.assertTrue(result)
        self.action_dto = self.action_dao.get("navigation")
        self.assertEqual("""\
(:durative-action navigation
\t:parameters ( ?r - robot ?s - wp ?d - wp)
\t:duration (= ?duration 10)
\t:condition (and
\t\t(at start (at ?r ?s))
\t\t(at start (> (battery_level ?r) 30.00))
\t)
\t:effect (and
\t\t(at end (not (at ?r ?s)))
\t\t(at end (at ?r ?d))
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
        self.action_dto.durative = False
        self.condition_1.time = ""
        self.condition_2.time = ""
        self.effect_1.time = ""
        self.effect_2.time = ""
        self.effect_3.time = ""

        self.action_dao._save(self.action_dto)
        result = self.action_dao._update(self.action_dto)
        self.assertTrue(result)

        self.action_dto = self.action_dao.get("navigation")
        self.assertEqual("""\
(:action navigation
\t:parameters ( ?r - robot ?s - wp ?d - wp)
\t:precondition (and
\t\t(at ?r ?s)
\t\t(> (battery_level ?r) 30.00)
\t)
\t:effect (and
\t\t(not (at ?r ?s))
\t\t(at ?r ?d)
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

    def test_action_dao_modify_fluent_type(self):
        self.action_dao._save(self.action_dto)

        self.action_dto = self.action_dao.get("navigation")
        self.action_dto.conditions[0].fluent.name = "bot_at"
        self.action_dto.parameters[0].type.name = "bot"

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
