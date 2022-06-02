
""" Mongo Dao Action """


from typing import List

from kant.kant_dao.dao_interface import ActionDao
from kant.kant_dao.mongo_dao import(
    MongoDao,
    MongoFactDao,
    MongoTypeDao,
    MongoFluentDao
)

from kant.kant_dao.mongo_dao.mongo_models import (
    ActionModel,
    ConditionEffectModel,
    ParameterModel
)
from kant.kant_dao.mongo_dao.mongo_object_dao import MongoObjectDao

from kant.kant_dto import (
    ConditionEffectDto,
    ActionDto,
    ObjectDto
)
from kant.kant_dto.fluent_dto import FluentDto
from kant.kant_dto.type_dto import TypeDto


class MongoActionDao(ActionDao, MongoDao):
    """ Mongo Dao Action Class """

    def __init__(self, uri: str = None, connect: bool = True):

        ActionDao.__init__(self)
        MongoDao.__init__(self, uri, connect)

        self._me_type_dao = MongoTypeDao(uri, connect=False)
        self._me_fluent_dao = MongoFluentDao(uri, connect=False)

    @staticmethod
    def __condition_effect_model_to_dto(condition_effect_model: ConditionEffectModel,
                                        parameter_dict: dict) -> ConditionEffectDto:
        """ convert a Mongoengine condition/effect document into a ConditionEffectDto

        Args:
            condition_effect_model
            (ConditionEffectModel): Mongoengine condition/effect document

        Returns:
            ConditionEffectDto: ConditionEffectDto
        """

        fluent_dto = MongoFluentDao._model_to_dto(
            condition_effect_model.fluent)

        condition_effect_dto = ConditionEffectDto(
            fluent_dto,
            condition_effect=condition_effect_model.condition_effect,
            time=condition_effect_model.time)

        if fluent_dto.is_numeric:
            condition_effect_dto.value = condition_effect_model.numeric_value
        else:
            condition_effect_dto.value = condition_effect_model.bool_value

        object_dto_list = []

        for parameter_model in condition_effect_model.parameters:
            object_dto = parameter_dict[parameter_model.name]
            object_dto_list.append(object_dto)

        condition_effect_dto.objects = object_dto_list

        return condition_effect_dto

    @staticmethod
    def _model_to_dto(action_model: ActionModel) -> ActionDto:
        """ convert a Mongoengine action document into a ActionDto

        Args:
            action_model (ActionModel): Mongoengine action document

        Returns:
            ActionDto: ActionDto
        """

        action_dto = ActionDto(action_model.action_name)
        action_dto.duration = action_model.duration
        action_dto.durative = action_model.durative

        parameters_list = []
        conditions_list = []
        effects_list = []
        parameter_dict = {}

        # ACTION PARAMS
        for parameter_model in action_model.parameters:
            object_dto = MongoObjectDao._model_to_dto(parameter_model)
            parameter_dict[parameter_model.name] = object_dto
            parameters_list.append(object_dto)

        # ACTION CONDIS
        for condition_model in action_model.conditions:
            condition_effect_dto = MongoActionDao.__condition_effect_model_to_dto(
                condition_model, parameter_dict)
            conditions_list.append(condition_effect_dto)

        # ACTION EFFECTS
        for effect_model in action_model.effects:
            condition_effect_dto = MongoActionDao.__condition_effect_model_to_dto(
                effect_model, parameter_dict)
            effects_list.append(condition_effect_dto)

        # SET SAME OBJECT FOR FLUENTS AND TYPES

        fluent_dict = {}
        type_dict = {}

        # conditions/effct
        for condition_effect_dto in list(conditions_list + effects_list):

            fluent_dto: FluentDto = condition_effect_dto.fluent

            # new fluent
            if not fluent_dto.name in fluent_dict:

                type_list = []
                for type_dto in fluent_dto.types:

                    # new type
                    if not type_dto.name in type_dict:
                        type_dict[type_dto.name] = type_dto

                    # type already exists
                    else:
                        type_dto = type_dict[type_dto.name]

                    type_list.append(type_dto)

                fluent_dto.types = type_list
                fluent_dict[fluent_dto.name] = fluent_dto

            # fluent alrredy exists
            else:
                fluent_dto = fluent_dict[fluent_dto.name]

            condition_effect_dto.fluent = fluent_dto

        # parameters
        for parameter_dto in parameters_list:

            type_dto: TypeDto = parameter_dto.type

            if not type_dto.name in type_dict:
                type_dict[type_dto.name] = type_dto
            else:
                type_dto = type_dict[type_dto.name]
                parameter_dto.type = type_dto

        action_dto.parameters = parameters_list
        action_dto.conditions = conditions_list
        action_dto.effects = effects_list

        return action_dto

    @staticmethod
    def __condition_effect_dto_to_model(condition_effect_dto: ConditionEffectDto,
                                        parameter_dict: dict) -> ConditionEffectModel:
        """ convert a ConditionEffectDto into a Mongoengine condition/effect document

        Args:
            condition_effect_dto (ConditionEffectDto): ConditionEffectDto

        Returns:
            Document: Mongoengine condition/effect document
        """

        fluent_model = MongoFluentDao._dto_to_model(
            condition_effect_dto.fluent)

        condition_model = ConditionEffectModel()
        condition_model.fluent = fluent_model
        condition_model.time = condition_effect_dto.time
        condition_model.condition_effect = condition_effect_dto.condition_effect

        if condition_effect_dto.fluent.is_numeric:
            condition_model.numeric_value = condition_effect_dto.value
        else:
            condition_model.bool_value = condition_effect_dto.value

        # params
        for param in condition_effect_dto.objects:
            condition_model.parameters.append(
                parameter_dict[param.name])

        return condition_model

    @staticmethod
    def _dto_to_model(action_dto: ActionDto) -> ActionModel:
        """ convert a ActionDto into a Mongoengine action document

        Args:
            action_dto (ActionDto): ActionDto

        Returns:
            Document: Mongoengine action document
        """

        action_model = ActionModel()

        action_model.action_name = action_dto.name
        action_model.duration = action_dto.duration
        action_model.durative = action_dto.durative

        parameter_dict = {}

        # ACTION PARAMS
        for param in action_dto.parameters:
            type_model = MongoTypeDao._dto_to_model(param.type)

            param_name = param.name

            parameter_model = ParameterModel()
            parameter_model.name = param_name
            parameter_model.type = type_model

            action_model.parameters.append(
                parameter_model)

            parameter_dict[param_name] = parameter_model

        # ACTION CONDIS
        for condition_dto in action_dto.conditions:
            condition_model = MongoActionDao.__condition_effect_dto_to_model(
                condition_dto, parameter_dict)

            action_model.conditions.append(condition_model)

            if condition_model.fluent not in action_model._fluents:
                action_model._fluents.append(
                    condition_model.fluent)

        # ACTION EFFECTS
        for effect_dto in action_dto.effects:
            effect_model = MongoActionDao.__condition_effect_dto_to_model(
                effect_dto, parameter_dict)

            action_model.effects.append(effect_model)

            if condition_model.fluent not in action_model._fluents:
                action_model._fluents.append(
                    effect_model.fluent)

        return action_model

    @staticmethod
    def _check_condition_efect_dto(condition_effect_dto: ConditionEffectDto,
                                   parameter_dtos: ObjectDto) -> bool:
        """ check if the types of the objects of a codition/effect dto are
            the same as the types of its fluent and if that objects are action parameters

        Args:
            condition_effect_dto
            (ConditionEffectDto): ConditionEffectDto

            parameter_dtos
            (ObjectDto): ObjectDto

        Returns:
            bool: condition/effect is correct?
        """

       # check if fact is correct
        if(len(condition_effect_dto.objects) !=
           len(condition_effect_dto.fluent.types)):
            return False

        object_dtos = condition_effect_dto.objects
        type_dtos = condition_effect_dto.fluent.types

        for object_dto, type_dto in zip(object_dtos, type_dtos):

            # check if condition/effect object type is a parameter
            if not object_dto in parameter_dtos:
                return False

            # check if condition/effect object type is correct
            if not MongoFactDao._check_type_dto(object_dto.type, type_dto):
                return False

        return True

    @staticmethod
    def _check_action_dto(action_dto: ActionDto) -> bool:
        """ check if a ActionDto is correct:
            condition and effect must be correct (similar to fact)

        Args:
            action_dto (ActionDto): ActionDto to check

        Returns:
            bool: is ActionDto correct?
        """

        for condi_effect_dto in (action_dto.conditions +
                                 action_dto.effects):
            if(not action_dto.durative and condi_effect_dto.time):
                return False
            elif(action_dto.durative and not condi_effect_dto.time):
                return False

            if not MongoActionDao._check_condition_efect_dto(condi_effect_dto,
                                                             action_dto.parameters):
                return False

        return True

    def _exist_in_mongo(self, action_dto: ActionDto) -> bool:
        """ check if ActionDto exists

        Args:
            action_dto (ActionDto): ActionDto

        Returns:
            bool: ActionDto exists?
        """

        if self._get_model(action_dto):
            return True
        return False

    def _get_model(self, action_dto: ActionDto) -> ActionModel:
        """ get the Mongoengine action document corresponding to a give ActionDto

        Args:
            action_dto (ActionDto): ActionDto

        Returns:
            Document: Mongoengine action document
        """

        action_model = ActionModel.objects(
            action_name=action_dto.name)
        if not action_model:
            return None
        return action_model[0]

    def get(self, action_name: str) -> ActionDto:
        """ get a ActionDto with a given action name
            return None if there is no with that action name

        Args:
            action_name (str): action name

        Returns:
            ActionDto: ActionDto of the action name
        """

        action_model = ActionModel.objects(
            action_name=action_name)

        # check if action exists
        if action_model:

            action_model = action_model[0]
            action_dto = MongoActionDao._model_to_dto(action_model)

            if not MongoActionDao._check_action_dto(action_dto):
                return None

            return action_dto

        return None

    def get_all(self) -> List[ActionDto]:
        """ get all ActionDto

        Returns:
            List[ActionDto]: list of all ActionDto
        """

        action_model = ActionModel.objects.order_by("action_name")
        action_dto_list = []

        for ele in action_model:
            action_dto = MongoActionDao._model_to_dto(ele)
            if MongoActionDao._check_action_dto(action_dto):
                action_dto_list.append(action_dto)

        return action_dto_list

    def _save(self, action_dto: ActionDto) -> bool:
        """ save a ActionDto
            if the ActionDto is already saved return False, else return True

        Args:
            action_dto (ActionDto): ActionDto to save

        Returns:
            bool: succeed
        """

        if not self._check_action_dto(action_dto):
            return False

        if self._exist_in_mongo(action_dto):
            return False

        action_model = self._dto_to_model(
            action_dto)

        # propagate saving
        for parameter_dto in action_dto.parameters:
            if not self._me_type_dao.save(parameter_dto.type):
                return False

        for fluent_model in action_model._fluents:

            fluent_dto = MongoFluentDao._model_to_dto(fluent_model)

            if not self._me_fluent_dao.save(fluent_dto):
                return False

        # saving
        action_model.save()

        return True

    def _update(self, action_dto: ActionDto) -> bool:
        """ update a ActionDto
            if the ActionDto is not saved return False, else return True

        Args:
            action_dto (ActionDto): ActionDto to update

        Returns:
            bool: succeed
        """

        if not self._check_action_dto(action_dto):
            return False

        action_model = self._get_model(action_dto)

        # check if action exists
        if action_model:

            # propagate saving
            for parameter_dto in action_dto.parameters:
                if not self._me_type_dao.save(parameter_dto.type):
                    return False

            for fluent_model in action_model._fluents:

                fluent_dto = MongoFluentDao._model_to_dto(fluent_model)

                if not self._me_fluent_dao.save(fluent_dto):
                    return False

            # updating
            new_action_model = MongoActionDao._dto_to_model(action_dto)

            action_model.action_name = new_action_model.action_name
            action_model.durative = new_action_model.durative
            action_model.duration = new_action_model.duration
            action_model.parameters = new_action_model.parameters
            action_model.conditions = new_action_model.conditions
            action_model.effects = new_action_model.effects
            action_model.save()

            return True

        return False

    def save(self, action_dto: ActionDto) -> bool:

        if self._exist_in_mongo(action_dto):
            return self._update(action_dto)

        return self._save(action_dto)

    def delete(self, action_dto: ActionDto) -> bool:
        """ save or update a ActionDto
            if the ActionDto is not saved it will be saved, else it will be updated

        Args:
            action_dto (ActionDto): ActionDto to save or update

        Returns:
            bool: succeed
        """

        action_model = self._get_model(action_dto)

        # check if action exists
        if action_model:
            action_model.delete()
            return True

        return False

    def delete_all(self) -> bool:
        """ delete all actions

        Returns:
            bool: succeed
        """

        action_dto_list = self.get_all()

        for ele in action_dto_list:
            self.delete(ele)

        return True
