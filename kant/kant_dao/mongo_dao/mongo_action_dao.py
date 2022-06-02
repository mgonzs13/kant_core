
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

from kant.kant_dto import (
    ConditionEffectDto,
    ActionDto,
    ObjectDto
)


class MongoActionDao(ActionDao, MongoDao):
    """ Mongo Dao Action Class """

    def __init__(self, uri: str = None, connect: bool = True):

        ActionDao.__init__(self)
        MongoDao.__init__(self, uri, connect)

        self._me_type_dao = MongoTypeDao(uri, connect=False)
        self._me_fluent_dao = MongoFluentDao(uri, connect=False)

    def __condition_effect_model_to_dto(self,
                                        condition_effect_model: ConditionEffectModel,
                                        parameter_dict: dict) -> ConditionEffectDto:
        """ convert a Mongoengine condition/effect document into a ConditionEffectDto

        Args:
            condition_effect_model
            (ConditionEffectModel): Mongoengine condition/effect document

        Returns:
            ConditionEffectDto: ConditionEffectDto
        """

        fluent_dto = self._me_fluent_dao.get(
            condition_effect_model.fluent.name)

        condition_effect_dto = ConditionEffectDto(
            fluent_dto,
            condition_effect=condition_effect_model.condition_effect,
            time=condition_effect_model.time)

        if fluent_dto.get_is_numeric():
            condition_effect_dto.set_value(
                condition_effect_model.numeric_value)
        else:
            condition_effect_dto.set_value(condition_effect_model.bool_value)

        object_dto_list = []

        for parameter_model in condition_effect_model.parameters:
            object_dto = parameter_dict[parameter_model.name]
            object_dto_list.append(object_dto)

        condition_effect_dto.set_objects(object_dto_list)

        return condition_effect_dto

    def _model_to_dto(self, action_model: ActionModel) -> ActionDto:
        """ convert a Mongoengine action document into a ActionDto

        Args:
            action_model (ActionModel): Mongoengine action document

        Returns:
            ActionDto: ActionDto
        """

        action_dto = ActionDto(
            action_model.action_name)
        action_dto.set_duration(action_model.duration)
        action_dto.set_durative(action_model.durative)

        parameters_list = []
        conditions_list = []
        effects_list = []
        parameter_dict = {}

        # ACTION PARAMS
        for parameter_model in action_model.parameters:
            type_dto = self._me_type_dao.get(parameter_model.type.name)
            object_dto = ObjectDto(
                type_dto, parameter_model.name)
            parameter_dict[parameter_model.name] = object_dto
            parameters_list.append(object_dto)

        # ACTION CONDIS
        for condition_model in action_model.conditions:
            condition_effect_dto = self.__condition_effect_model_to_dto(
                condition_model, parameter_dict)
            conditions_list.append(condition_effect_dto)

        # ACTION EFFECTS
        for effect_model in action_model.effects:
            condition_effect_dto = self.__condition_effect_model_to_dto(
                effect_model, parameter_dict)
            effects_list.append(condition_effect_dto)

        # SET SAME OBJECT FOR FLUENTS AND TYPES

        fluent_dict = {}
        type_dict = {}

        # conditions/effct
        for condition_effect_dto in list(conditions_list + effects_list):

            fluent_dto = condition_effect_dto.get_fluent()

            # new fluent
            if not fluent_dto.get_name() in fluent_dict:

                type_list = []
                for type_dto in fluent_dto.get_types():

                    # new type
                    if not type_dto.get_name() in type_dict:
                        type_dict[type_dto.get_name()] = type_dto

                    # type already exists
                    else:
                        type_dto = type_dict[type_dto.get_name()]

                    type_list.append(type_dto)

                fluent_dto.set_types(type_list)
                fluent_dict[fluent_dto.get_name()] = fluent_dto

            # fluent alrredy exists
            else:
                fluent_dto = fluent_dict[fluent_dto.get_name()]

            condition_effect_dto.set_fluent(fluent_dto)

        # parameters
        for parameter_dto in parameters_list:

            type_dto = parameter_dto.get_type()

            if not type_dto.get_name() in type_dict:
                type_dict[type_dto.get_name()] = type_dto
            else:
                type_dto = type_dict[type_dto.get_name()]
                parameter_dto.set_type(type_dto)

        action_dto.set_parameters(parameters_list)
        action_dto.set_conditions(conditions_list)
        action_dto.set_effects(effects_list)

        return action_dto

    def __condition_effect_dto_to_model(self,
                                        condition_effect_dto: ConditionEffectDto,
                                        parameter_dict: dict) -> ConditionEffectModel:
        """ convert a ConditionEffectDto into a Mongoengine condition/effect document

        Args:
            condition_effect_dto (ConditionEffectDto): ConditionEffectDto

        Returns:
            Document: Mongoengine condition/effect document
        """

        fluent_model = self._me_fluent_dao._dto_to_model(
            condition_effect_dto.get_fluent())

        condition_model = ConditionEffectModel()
        condition_model.fluent = fluent_model
        condition_model.time = condition_effect_dto.get_time()
        condition_model.condition_effect = condition_effect_dto.get_condition_effect()

        if condition_effect_dto.get_fluent().get_is_numeric():
            condition_model.numeric_value = condition_effect_dto.get_value()
        else:
            condition_model.bool_value = condition_effect_dto.get_value()

        for param in condition_effect_dto.get_objects():

            condition_model.parameters.append(
                parameter_dict[param.get_name()])

        return condition_model

    def _dto_to_model(self, action_dto: ActionDto) -> ActionModel:
        """ convert a ActionDto into a Mongoengine action document

        Args:
            action_dto (ActionDto): ActionDto

        Returns:
            Document: Mongoengine action document
        """

        action_model = ActionModel()

        action_model.action_name = action_dto.get_name()
        action_model.duration = action_dto.get_duration()
        action_model.durative = action_dto.get_durative()

        parameter_dict = {}

        # ACTION PARAMS
        for param in action_dto.get_parameters():
            type_model = self._me_type_dao._dto_to_model(
                param.get_type())

            param_name = param.get_name()

            parameter_model = ParameterModel()
            parameter_model.name = param_name
            parameter_model.type = type_model

            action_model.parameters.append(
                parameter_model)

            parameter_dict[param_name] = parameter_model

        # ACTION CONDIS
        for condition_dto in action_dto.get_conditions():
            condition_model = self.__condition_effect_dto_to_model(
                condition_dto, parameter_dict)

            action_model.conditions.append(condition_model)

            if condition_model.fluent not in action_model._fluents:
                action_model._fluents.append(
                    condition_model.fluent)

        # ACTION EFFECTS
        for effect_dto in action_dto.get_effects():
            effect_model = self.__condition_effect_dto_to_model(
                effect_dto, parameter_dict)

            action_model.effects.append(effect_model)

            if condition_model.fluent not in action_model._fluents:
                action_model._fluents.append(
                    effect_model.fluent)

        return action_model

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
            action_name=action_dto.get_name())
        if not action_model:
            return None
        return action_model[0]

    def _check_condition_efect_dto(self,
                                   condition_effect_dto: ConditionEffectDto,
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
        if(len(condition_effect_dto.get_objects()) !=
           len(condition_effect_dto.get_fluent().get_types())):
            return False

        object_dtos = condition_effect_dto.get_objects()
        type_dtos = condition_effect_dto.get_fluent().get_types()

        for object_dto, type_dto in zip(object_dtos, type_dtos):

            # check if condition/effect object type is a parameter
            if not object_dto in parameter_dtos:
                return False

            # check if condition/effect object type is correct
            if not MongoFactDao._check_type_dto(object_dto.get_type(), type_dto):
                return False

        return True

    def _check_action_dto(self, action_dto: ActionDto) -> bool:
        """ check if a ActionDto is correct:
            condition and effect must be correct (similar to fact)

        Args:
            action_dto (ActionDto): ActionDto to check

        Returns:
            bool: is ActionDto correct?
        """

        for condi_effect_dto in (action_dto.get_conditions() +
                                 action_dto.get_effects()):
            if(not action_dto.get_durative() and condi_effect_dto.get_time()):
                return False
            elif(action_dto.get_durative() and not condi_effect_dto.get_time()):
                return False

            if not self._check_condition_efect_dto(condi_effect_dto,
                                                   action_dto.get_parameters()):
                return False

        return True

    def _check_condition_efect_model(self,
                                     condition_effect_model: ConditionEffectModel,
                                     parameter_models: ParameterModel) -> bool:
        """ check if the types of the objects of a codition/effect model are
            the same as the types of its fluent and if that objects are action parameters

        Args:
            condition_effect_model
            (ConditionEffectModel): Mongoengine condition/effect document

            parameter_models
            (ParameterModel): Mongoengine parameter documents

        Returns:
            bool: condition/effect is correct?
        """

        # check if fact is correct
        if(len(condition_effect_model.parameters) !=
           len(condition_effect_model.fluent.types)):
            return False

        parameter_models = condition_effect_model.parameters
        type_models = condition_effect_model.fluent.types

        for parameter_model, type_model in zip(parameter_models, type_models):

            if not parameter_model in parameter_models:
                return False

            # check if fact is correct
            if not MongoFactDao._check_type_model(parameter_model.type, type_model):
                return False

        return True

    def _check_action_model(self, action_model: ActionModel) -> bool:
        """ check if a ActionDto is correct:
            condition and effect must be correct (similar to fact)

        Args:
            action_dto (ActionDto): ActionDto to check

        Returns:
            bool: is ActionDto correct?
        """

        for condi_effect_model in (action_model.conditions +
                                   action_model.effects):
            if(not action_model.durative and condi_effect_model.time):
                return False
            elif(action_model.durative and not condi_effect_model.time):
                return False

            if not self._check_condition_efect_model(condi_effect_model,
                                                     action_model.parameters):
                return False

        return True

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

            if not self._check_action_model(action_model):
                return None

            action_dto = self._model_to_dto(
                action_model)
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
            if self._check_action_model(ele):
                action_dto = self._model_to_dto(ele)
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
        for parameter_dto in action_dto.get_parameters():
            if not self._me_type_dao.save(parameter_dto.get_type()):
                return False

        for fluent_model in action_model._fluents:

            fluent_dto = self._me_fluent_dao._model_to_dto(fluent_model)

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
            for parameter_dto in action_dto.get_parameters():
                if not self._me_type_dao.save(parameter_dto.get_type()):
                    return False

            for fluent_model in action_model._fluents:

                fluent_dto = self._me_fluent_dao._model_to_dto(fluent_model)

                if not self._me_fluent_dao.save(fluent_dto):
                    return False

            # updating
            new_action_model = self._dto_to_model(action_dto)

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
