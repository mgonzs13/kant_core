
""" Mongo Fact Dao """

from typing import List, Dict

from kant.kant_dao.dao_interface import FactDao
from kant.kant_dao.mongo_dao import (
    MongoDao,
    MongoFluentDao,
    MongoObjectDao
)

from kant.kant_dao.mongo_dao.mongo_models import (
    FactModel,
    TypeModel
)

from kant.kant_dto import FactDto
from kant.kant_dto.type_dto import TypeDto


class MongoFactDao(FactDao, MongoDao):
    """ Mongo Fact Dao Class """

    def __init__(self, uri: str = None, connect: bool = True) -> None:

        FactDao.__init__(self)
        MongoDao.__init__(self, uri, connect)

        self._me_object_dao = MongoObjectDao(uri, connect=False)
        self._me_fluent_dao = MongoFluentDao(
            uri, connect=False)

    @staticmethod
    def _check_type_model(type_model_1: TypeModel, type_model_2: TypeModel) -> bool:
        """ check if a type is or inherit from another type

          Args:
              type_dto_1 (TypeModel): type to check
              type_dto_2 (TypeModel): target type

          Returns:
              bool: is or inherit?
        """

        if type_model_1.name == type_model_2.name:
            return True
        else:
            if not type_model_1.father is None:
                return MongoFactDao._check_type_model(type_model_1.father, type_model_2)
            else:
                return False

    def _check_fact_model(self, fact_model: FactModel) -> bool:
        """ check if the types of the objects of a fact model are
            the same as the types of its fluent

        Args:
            fact_model (FactModel): Mongoengine fact document

        Returns:
            bool: poposition is correct?
        """

        # check if fact is correct
        if(len(fact_model.arguments) !=
           len(fact_model.fluent.types)):
            return False

        object_models = fact_model.arguments
        type_models = fact_model.fluent.types

        for object_model, type_model in zip(object_models, type_models):

            # check if fact is correct
            if not MongoFactDao._check_type_model(object_model.type, type_model):
                return False

        return True

    @staticmethod
    def _add_fathers(type_dto: TypeDto, type_dict: Dict[str, TypeDto]) -> None:
        """ add recursively type fathers to a dictionary

        Args:
            type_dto (TypeDto): starter type
            type_dict (Dict[str, TypeDto]): dictionary
        """

        if not type_dto.get_name() in type_dict:
            type_dict[type_dto.get_name()] = type_dto

        if not type_dto.get_father() is None:
            MongoFactDao._add_fathers(type_dto.get_father(), type_dict)

    def _model_to_dto(self, fact_model: FactModel) -> FactDto:
        """ convert a Mongoengine type document into a FactDto

        Args:
            fact_model (FactModel): Mongoengine fact document

        Returns:
            FactDto: FactDto
        """

        object_list = []
        type_dict = {}

        fluent_dto = self._me_fluent_dao._model_to_dto(
            fact_model.fluent)

        for type_dto in fluent_dto.get_types():
            type_dict[type_dto.get_name()] = type_dto

        for object_model in fact_model.arguments:

            object_dto = self._me_object_dao._model_to_dto(
                object_model)

            self._add_fathers(object_dto.get_type(), type_dict)

            object_dto.set_type(
                type_dict[object_dto.get_type().get_name()])

            object_list.append(object_dto)

        fact_dto = FactDto(
            fluent_dto, object_list)

        fact_dto.set_is_goal(
            fact_model.is_goal)

        if fact_dto.get_fluent().get_is_numeric():
            fact_dto.set_value(fact_model.numeric_value)
        else:
            fact_dto.set_value(fact_model.bool_value)

        return fact_dto

    @staticmethod
    def _check_type_dto(type_dto_1: TypeDto, type_dto_2: TypeDto) -> bool:
        """ check if a type is or inherit from another type

        Args:
            type_dto_1 (TypeDto): type to check
            type_dto_2 (TypeDto): target type

        Returns:
            bool: is or inherit?
        """

        if type_dto_1 == type_dto_2:
            return True
        else:
            if not type_dto_1.get_father() is None:
                return MongoFactDao._check_type_dto(type_dto_1.get_father(), type_dto_2)
            else:
                return False

    def _check_fact_dto(self, fact_dto: FactDto) -> bool:
        """ check if the types of the objects of a fact dto are
            the same as the types of its fluent

        Args:
            fact_dto (FactDto): fact dto

        Returns:
            bool: poposition is correct?
        """

       # check if fact is correct
        if(len(fact_dto.get_objects()) !=
           len(fact_dto.get_fluent().get_types())):
            return False

        object_dtos = fact_dto.get_objects()
        type_dtos = fact_dto.get_fluent().get_types()

        for object_dto, type_dto in zip(object_dtos, type_dtos):

            # check if fact is correct
            if not MongoFactDao._check_type_dto(object_dto.get_type(), type_dto):
                return False

        return True

    def _dto_to_model(self, fact_dto: FactDto) -> FactModel:
        """ convert a FactDto into a Mongoengine propostion document

        Args:
            fact_dto (FactDto): FactDto

        Returns:
            Document: Mongoengine propostion document
        """

        fact_model = FactModel()

        # fluent model
        fluent_model = self._me_fluent_dao._dto_to_model(
            fact_dto.get_fluent())

        fact_model.fluent = fluent_model

        # is goal
        fact_model.is_goal = fact_dto.get_is_goal()

        # value
        if fact_dto.get_fluent().get_is_numeric():
            fact_model.numeric_value = fact_dto.get_value()
        else:
            fact_model.bool_value = fact_dto.get_value()

        # objects models
        for object_dto in fact_dto.get_objects():

            object_model = self._me_object_dao._dto_to_model(
                object_dto)

            fact_model.arguments.append(
                object_model)

        return fact_model

    def _exist_in_mongo(self, fact_dto: FactDto) -> bool:
        """ check if FactDto exists

        Args:
            fact_dto (FactDto): FactDto

        Returns:
            bool: FactDto exists?
        """

        if self._get_model(fact_dto):
            return True
        return False

    def _get_model(self, fact_dto: FactDto) -> FactModel:
        """ get the Mongoengine fact document corresponding to a give FactDto

        Args:
            fact_dto (FactDto): FactDto

        Returns:
            Document: Mongoengine fact document
        """

        objects_dto_list = fact_dto.get_objects()

        objects_list = []
        for object_dto in objects_dto_list:
            objects_list.append(object_dto.get_name())

        # getting fact
        fact_model = FactModel.objects(
            fluent=fact_dto.get_fluent().get_name(),
            arguments=objects_list,
            is_goal=fact_dto.get_is_goal())

        # check if fact exist
        if not fact_model:
            return None

        return fact_model[0]

    def get_by_fluent(self, fluent_name: str) -> List[FactDto]:
        """ get all FactDto with a given fluent name

        Args:
            fluent_name (str): fluent name

        Returns:
            List[FactDto]: list of FactDto
        """

        fact_model = FactModel.objects(
            fluent=fluent_name)

        fact_dto_list = []

        for ele in fact_model:
            if self._check_fact_model(ele):
                fact_dto_list.append(self._model_to_dto(ele))

        return fact_dto_list

    def _get_all(self, is_goal: bool = None) -> List[FactDto]:
        """ get all FactDto
            is_goal == None -> get all fact
            is_goal == True -> gel all goals
            is_goal == False -> getl no goals

        Args:
            is_goal (bool, optional): get all, all goals, all no goals?. Defaults to None.

        Returns:
            List[FactDto]: list of FactDto
        """

        if(is_goal is None):
            fact_model = FactModel.objects()
        else:
            fact_model = FactModel.objects(
                is_goal=is_goal)

        fact_dto_list = []

        for ele in fact_model:
            if self._check_fact_model(ele):
                fact_dto_list.append(self._model_to_dto(ele))

        return fact_dto_list

    def get_goals(self) -> List[FactDto]:
        """ get all FactDto that are goals

        Returns:
            List[FactDto]: list of FactDto
        """

        return self._get_all(is_goal=True)

    def get_no_goals(self) -> List[FactDto]:
        """ get all FactDto that are not goals

        Returns:
            List[FactDto]: list of FactDto
        """

        return self._get_all(is_goal=False)

    def get_all(self) -> List[FactDto]:
        """ get all FactDto

        Returns:
            List[FactDto]: list of FactDto
        """

        return self._get_all()

    def get_propositions(self) -> List[FactDto]:
        """ get all propositions (facts with bool value)

        Returns:
            List[FactDto]: list of FactDto
        """

        fact_list = self.get_no_goals()

        proposition_list = []
        for ele in fact_list:
            if not ele.get_fluent().get_is_numeric():
                proposition_list.append(ele)

        return proposition_list

    def get_functions(self) -> List[FactDto]:
        """ get all functions (facts with numeric value)

        Returns:
            List[FactDto]: list of FactDto
        """

        fact_list = self.get_no_goals()

        numeric_list = []
        for ele in fact_list:
            if ele.get_fluent().get_is_numeric():
                numeric_list.append(ele)

        return numeric_list

    def _save(self, fact_dto: FactDto) -> bool:
        """ save a FactDto
            if the FactDto is already saved return False, else return True

        Args:
            fact_dto (FactDto): FactDto to save

        Returns:
            bool: succeed
        """

        if self._exist_in_mongo(fact_dto):
            return False

        if not self._check_fact_dto(fact_dto):
            return False

       # propagating saving
        for object_dto in fact_dto.get_objects():
            if not self._me_object_dao.save(object_dto):
                return False

        if not self._me_fluent_dao.save(fact_dto.get_fluent()):
            return False

        # saving
        fact_model = self._dto_to_model(
            fact_dto)

        fact_model.save(cascade=True)
        return True

    def _update(self, fact_dto: FactDto) -> bool:
        """ update a FactDto
            if the FactDto is not saved return False, else return True

        Args:
            fact_dto (FactDto): FactDto to update

        Returns:
            bool: succeed
        """

        if not self._check_fact_dto(fact_dto):
            return False

        fact_model = self._get_model(
            fact_dto)

        # check if fact exists
        if fact_model:

            # propagating saving
            for object_dto in fact_dto.get_objects():
                if not self._me_object_dao.save(object_dto):
                    return False

            if not self._me_fluent_dao.save(fact_dto.get_fluent()):
                return False

            # updating
            new_fact_model = self._dto_to_model(
                fact_dto)
            fact_model.fluent = new_fact_model.fluent
            fact_model.arguments = new_fact_model.arguments
            fact_model.is_goal = new_fact_model.is_goal
            fact_model.save()

            return True

        return False

    def save(self, fact_dto: FactDto) -> bool:
        """ save or update a FactDto
            if the FactDto is not saved it will be saved, else it will be updated

        Args:
            fact_dto (FactDto): FactDto to save or update

        Returns:
            bool: succeed
        """

        if self._exist_in_mongo(fact_dto):
            return self._update(fact_dto)

        return self._save(fact_dto)

    def delete(self, fact_dto: FactDto) -> bool:
        """ delete a FactDto
            if the FactDto is not saved return False, else return True

        Args:
            fact_dto (FactDto): FactDto to delete

        Returns:
            bool: succeed
        """

        fact_model = self._get_model(
            fact_dto)

        # check if fact exists
        if fact_model:
            fact_model.delete()
            return True

        return False

    def delete_all(self) -> bool:
        """ delete all facts

        Returns:
            bool: succeed
        """

        fact_dto_list = self.get_all()

        for ele in fact_dto_list:
            self.delete(ele)

        return True
