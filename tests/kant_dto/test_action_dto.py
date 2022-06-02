from calendar import c
import unittest
from kant.kant_dto.type_dto import TypeDto
from kant.kant_dto.fluent_dto import FluentDto
from kant.kant_dto.action_dto import ActionDto
from kant.kant_dto.object_dto import ObjectDto
from kant.kant_dto.condition_effect_dto import ConditionEffectDto


class TestActionDto(unittest.TestCase):

    def setUp(self):

        self.robot_type = TypeDto("robot")
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
                                              value=30)

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
                                           value=10)

        self.action_dto = ActionDto(
            "navigation", [r, s, d],
            [self.condition_1, self.condition_2],
            [self.effect_1, self.effect_2, self.effect_3])

    def test_action_dto_str(self):
        self.maxDiff = None
        self.action_dto.durative = False
        self.condition_1.time = ""
        self.condition_2.time = ""
        self.effect_1.time = ""
        self.effect_2.time = ""
        self.effect_3.time = ""
        self.assertEqual("""\
(:action navigation
\t:parameters ( ?r - robot ?s - wp ?d - wp)
\t:precondition (and
\t\t(robot_at ?r ?s)
\t\t(> (battery_level ?r) 30)
\t)
\t:effect (and
\t\t(not (robot_at ?r ?s))
\t\t(robot_at ?r ?d)
\t\t(decrease (battery_level ?r) 10)
\t)
)""",
                         str(self.action_dto))

    def test_action_dto_str_durative(self):
        self.maxDiff = None
        self.assertEqual("""\
(:durative-action navigation
\t:parameters ( ?r - robot ?s - wp ?d - wp)
\t:duration (= ?duration 10)
\t:condition (and
\t\t(at start (robot_at ?r ?s))
\t\t(at start (> (battery_level ?r) 30))
\t)
\t:effect (and
\t\t(at start (not (robot_at ?r ?s)))
\t\t(at end (robot_at ?r ?d))
\t\t(at end (decrease (battery_level ?r) 10))
\t)
)""",
                         str(self.action_dto))

    def test_action_dto_str_durative_no_effects(self):
        self.maxDiff = None
        self.action_dto.effects = []
        self.assertEqual("""\
(:durative-action navigation
\t:parameters ( ?r - robot ?s - wp ?d - wp)
\t:duration (= ?duration 10)
\t:condition (and
\t\t(at start (robot_at ?r ?s))
\t\t(at start (> (battery_level ?r) 30))
\t)
\t:effect (and
\t)
)""",
                         str(self.action_dto))

    def test_action_dto_str_durative_no_conditions(self):
        self.maxDiff = None
        self.action_dto.conditions = []
        self.assertEqual("""\
(:durative-action navigation
\t:parameters ( ?r - robot ?s - wp ?d - wp)
\t:duration (= ?duration 10)
\t:condition (and
\t)
\t:effect (and
\t\t(at start (not (robot_at ?r ?s)))
\t\t(at end (robot_at ?r ?d))
\t\t(at end (decrease (battery_level ?r) 10))
\t)
)""",
                         str(self.action_dto))

    def test_action_dto_str_durative_no_parameters(self):
        self.maxDiff = None
        self.action_dto.conditions = []
        self.action_dto.effects = []
        self.action_dto.parameters = []
        self.assertEqual("""\
(:durative-action navigation
\t:parameters ()
\t:duration (= ?duration 10)
\t:condition (and
\t)
\t:effect (and
\t)
)""",
                         str(self.action_dto))

    def test_action_dto_get_name(self):
        self.assertEqual("navigation", self.action_dto.name)

    def test_action_dto_get_prameters_list(self):
        params_list = self.action_dto.parameters
        self.assertEqual("r - robot", str(params_list[0]))
        self.assertEqual("s - wp", str(params_list[1]))
        self.assertEqual("d - wp", str(params_list[2]))

    def test_action_dto_get_conditions(self):
        conditions_list = self.action_dto.conditions
        self.assertEqual("(at start (robot_at ?r ?s))",
                         str(conditions_list[0]))
        self.assertEqual("(at start (> (battery_level ?r) 30))",
                         str(conditions_list[1]))

    def test_action_dto_get_effects(self):
        effects_list = self.action_dto.effects
        self.assertEqual("(at start (not (robot_at ?r ?s)))",
                         str(effects_list[0]))
        self.assertEqual("(at end (robot_at ?r ?d))",
                         str(effects_list[1]))

    def test_action_dto_get_durative(self):
        self.assertTrue(self.action_dto.durative)

    def test_action_dto_get_duration(self):
        self.assertEqual(10, self.action_dto.duration)

    def test_action_dto_eq_true(self):
        action_dto = ActionDto("navigation")
        result = (self.action_dto == action_dto)
        self.assertTrue(result)

    def test_action_dto_eq_false_bad_action_name(self):
        action_dto = ActionDto("other")
        result = (self.action_dto == action_dto)
        self.assertFalse(result)

    def test_action_dto_eq_false_bad_instance(self):
        result = (self.action_dto == 10)
        self.assertFalse(result)
