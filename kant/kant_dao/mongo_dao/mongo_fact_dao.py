
""" Mongo Fact Dao """

from typing import List, Dict

from kant.kant_dao.dao_interface import FactDao
from kant.kant_dao.mongo_dao import (
    MongoDao,
    MongoFluentDao,
    MongoObjectDao
)

from kant.kant_dao.mongo_dao.mongo_models import (
    FactModel
)

from kant.kant_dto import FactDto
from kant.kant_dto.type_dto import TypeDto


class MongoFactDao(FactDao, MongoDao):
    """ Mongo Fact Dao Class """

    def __init__(self, uri: str = None, connect: bool = True) -> None:

        FactDao.__init__(self)
        MongoDao.__init__(self, uri, connect)

        self._me_object_dao = MongoObjectDao(uri, connect=False)
        self._me_fluent_dao = MongoFluentDao(uri, connect=False)

    @staticmethod
    def _add_fathers(type_dto: TypeDto, type_dict: Dict[str, TypeDto]) -> None:
        """ add recursively type fathers to a dictionary

        Args:
            type_dto (TypeDto): starter type
            type_dict (Dict[str, TypeDto]): dictionary
        """

        if not type_dto.name in type_dict:
            type_dict[type_dto.name] = type_dto

        if not type_dto.father is None:
            MongoFactDao._add_fathers(type_dto.father, type_dict)

    @staticmethod
    def _model_to_dto(fact_model: FactModel) -> FactDto:
        """ convert a Mongoengine type document into a FactDto

        Args:
            fact_model (FactModel): Mongoengine fact document

        Returns:
            FactDto: FactDto
        """

        object_list = []
        type_dict = {}

        fluent_dto = MongoFluentDao._model_to_dto(fact_model.fluent)

        for type_dto in fluent_dto.types:
            type_dict[type_dto.name] = type_dto

        for object_model in fact_model.arguments:

            object_dto = MongoObjectDao._model_to_dto(
                object_model)

            MongoFactDao._add_fathers(object_dto.type, type_dict)

            object_dto.type = type_dict[object_dto.type.name]

            object_list.append(object_dto)

        fact_dto = FactDto(
            fluent_dto, object_list)

        fact_dto.is_goal = fact_model.is_goal

        if fact_dto.fluent.is_numeric:
            fact_dto.value = fact_model.numeric_value
        else:
            fact_dto.value = fact_model.bool_value

        return fact_dto

    @staticmethod
    def _dto_to_model(fact_dto: FactDto) -> FactModel:
        """ convert a FactDto into a Mongoengine propostion document

        Args:
            fact_dto (FactDto): FactDto

        Returns:
            Document: Mongoengine propostion document
        """

        fact_model = FactModel()

        # fluent model
        fluent_model = MongoFluentDao._dto_to_model(fact_dto.fluent)

        fact_model.fluent = fluent_model

        # is goal
        fact_model.is_goal = fact_dto.is_goal

        # value
        if fact_dto.fluent.is_numeric:
            fact_model.numeric_value = fact_dto.value
        else:
            fact_model.bool_value = fact_dto.value

        # objects models
        for object_dto in fact_dto.objects:

            object_model = MongoObjectDao._dto_to_model(object_dto)

            fact_model.arguments.append(
                object_model)

        return fact_model

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
            if not type_dto_1.father is None:
                return MongoFactDao._check_type_dto(type_dto_1.father, type_dto_2)
            else:
                return False

    def _check_fact_dto(fact_dto: FactDto) -> bool:
        """ check if the types of the objects of a fact dto are
            the same as the types of its fluent

        Args:
            fact_dto (FactDto): fact dto

        Returns:
            bool: poposition is correct?
        """

       # check if fact is correct
        if(len(fact_dto.objects) != len(fact_dto.fluent.types)):
            return False

        object_dtos = fact_dto.objects
        type_dtos = fact_dto.fluent.types

        for object_dto, type_dto in zip(object_dtos, type_dtos):
            # check if fact is correct
            if not MongoFactDao._check_type_dto(object_dto.type, type_dto):
                return False

        return True

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

        objects_dto_list = fact_dto.objects

        objects_list = []
        for object_dto in objects_dto_list:
            objects_list.append(object_dto.name)

        # getting fact
        fact_model = FactModel.objects(
            fluent=fact_dto.fluent.name,
            arguments=objects_list,
            is_goal=fact_dto.is_goal)

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
            fact_dto = MongoFactDao._model_to_dto(ele)
            if MongoFactDao._check_fact_dto(fact_dto):
                fact_dto_list.append(fact_dto)

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
            fact_dto = MongoFactDao._model_to_dto(ele)
            if MongoFactDao._check_fact_dto(fact_dto):
                fact_dto_list.append(fact_dto)

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

    def get_bool_facts(self) -> List[FactDto]:
        """ get all bool facts (facts with bool value)

        Returns:
            List[FactDto]: list of FactDto
        """

        fact_list = self.get_no_goals()

        proposition_list = []
        for ele in fact_list:
            if not ele.fluent.is_numeric:
                proposition_list.append(ele)

        return proposition_list

    def get_numeric_facts(self) -> List[FactDto]:
        """ get all numeric functions (facts with numeric value)

        Returns:
            List[FactDto]: list of FactDto
        """

        fact_list = self.get_no_goals()

        numeric_list = []
        for ele in fact_list:
            if ele.fluent.is_numeric:
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

        if not MongoFactDao._check_fact_dto(fact_dto):
            return False

       # propagating saving
        for object_dto in fact_dto.objects:
            if not self._me_object_dao.save(object_dto):
                return False

        if not self._me_fluent_dao.save(fact_dto.fluent):
            return False

        # saving
        fact_model = MongoFactDao._dto_to_model(
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

        if not MongoFactDao._check_fact_dto(fact_dto):
            return False

        fact_model = self._get_model(
            fact_dto)

        # check if fact exists
        if fact_model:

            # propagating saving
            for object_dto in fact_dto.objects:
                if not self._me_object_dao.save(object_dto):
                    return False

            if not self._me_fluent_dao.save(fact_dto.fluent):
                return False

            # updating
            new_fact_model = MongoFactDao._dto_to_model(
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
