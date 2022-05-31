
""" Mongo fluent Dao """

from typing import List

from kant.kant_dao.dao_interface import FluentDao
from kant.kant_dao.mongo_dao import (
    MongoDao,
    MongoTypeDao
)

from kant.kant_dao.mongo_dao.mongo_models import FluentModel

from kant.kant_dto import (
    FluentDto,
    TypeDto
)


class MongoFluentDao(FluentDao, MongoDao):
    """ Mongo fluent Dao Class """

    def __init__(self, uri: str = None, connect: bool = True) -> None:

        FluentDao.__init__(self)
        MongoDao.__init__(self, uri, connect)

        self._me_type_dao = MongoTypeDao(uri, connect=False)

    def _model_to_dto(self, fluent_model: FluentModel) -> FluentDto:
        """ convert a Mongoengine fluent document into a FluentDto

        Args:
            fluent_model (FluentModel): Mongoengine fluent document

        Returns:
            FluentDto: FluentDto
        """

        type_dto_list = []

        for type_model in fluent_model.types:
            type_dto = self._me_type_dao._model_to_dto(type_model)
            type_dto_list.append(type_dto)

        fluent_dto = FluentDto(
            fluent_model.name,
            type_dto_list,
            fluent_model.is_numeric)

        return fluent_dto

    def _dto_to_model(self, fluent_dto: FluentDto) -> FluentModel:
        """ convert a FluentDto into a Mongoengine fluent document

        Args:
            fluent_dto (FluentDto): FluentDto

        Returns:
            Document: Mongoengine fluent document
        """

        fluent_model = FluentModel()

        fluent_model.name = fluent_dto.get_name()
        fluent_model.is_numeric = fluent_dto.get_is_numeric()

        for type_dto in fluent_dto.get_types():

            type_model = self._me_type_dao._dto_to_model(
                type_dto)

            fluent_model.types.append(type_model)

        return fluent_model

    def _exist_in_mongo(self, fluent_dto: FluentDto) -> bool:
        """ check if FluentDto exists

        Args:
            fluent_dto (FluentDto): FluentDto

        Returns:
            bool: FluentDto exists?
        """

        if self._get_model(fluent_dto):
            return True
        return False

    def _get_model(self, fluent_dto: FluentDto) -> FluentModel:
        """ get the Mongoengine fluent document corresponding to a give FluentDto

        Args:
            fluent_dto (FluentDto): FluentDto

        Returns:
            Document: Mongoengine fluent document
        """

        fluent_model = FluentModel.objects(
            name=fluent_dto.get_name())

        if not fluent_model:
            return None

        return fluent_model[0]

    def get(self, fluent_name: str) -> FluentDto:
        """ get a FluentDto with a given fluent name
            return None if there is no with that fluent name

        Args:
            fluent_name (str): fluent name

        Returns:
            FluentDto: FluentDto of the fluent name
        """

        fluent_model = FluentModel.objects(
            name=fluent_name)

        # check if fluent exist
        if fluent_model:
            fluent_model = fluent_model[0]
            fluent_dto = self._model_to_dto(
                fluent_model)
            return fluent_dto

        return None

    def get_all(self) -> List[FluentDto]:
        """ get all FluentDto

        Returns:
            List[FluentDto]: list of all FluentDto
        """
        fluent_model = FluentModel.objects.order_by("name")
        fluent_dto_list = []

        for ele in fluent_model:
            fluent_dto = self._model_to_dto(ele)
            fluent_dto_list.append(fluent_dto)

        return fluent_dto_list

    def _save(self, fluent_dto: FluentDto) -> bool:
        """ save a FluentDto
            if the FluentDto is already saved return False, else return True

        Args:
            fluent_dto (FluentDto): FluentDto to save

        Returns:
            bool: succeed
        """

        if self._exist_in_mongo(fluent_dto):
            return False

        fluent_model = self._dto_to_model(
            fluent_dto)

        # propagating saving
        for type_dto in fluent_dto.get_types():
            if not self._me_type_dao.save(type_dto):
                return False

        # saving
        fluent_model.save(cascade=True)
        return True

    def _update(self, fluent_dto: FluentDto) -> bool:
        """ update a FluentDto
             if the FluentDto is not saved return False, else return True

         Args:
             fluent_dto (FluentDto): FluentDto to update

         Returns:
             bool: succeed
         """

        fluent_model = self._get_model(fluent_dto)

        # check if fluent exists
        if fluent_model:

            # propagating saving
            for type_dto in fluent_dto.get_types():
                if not self._me_type_dao.save(type_dto):
                    return False

            # updating
            new_fluent_model = self._dto_to_model(
                fluent_dto)
            fluent_model.name = new_fluent_model.name
            fluent_model.types = new_fluent_model.types
            fluent_model.save()

            return True

        return False

    def save(self, fluent_dto: FluentDto) -> bool:
        """ save or update a FluentDto
            if the FluentDto is not saved it will be saved, else it will be updated

        Args:
            fluent_dto (FluentDto): FluentDto to save or update

        Returns:
            bool: succeed
        """

        if self._exist_in_mongo(fluent_dto):
            return self._update(fluent_dto)

        return self._save(fluent_dto)

    def delete(self, fluent_dto: FluentDto) -> bool:
        """ delete a FluentDto
            if the FluentDto is not saved return False, else return True

        Args:
            fluent_dto (FluentDto): FluentDto to delete

        Returns:
            bool: succeed
        """

        fluent_model = self._get_model(fluent_dto)

        # check if fluent exists
        if fluent_model:
            fluent_model.delete()
            return True

        return False

    def delete_all(self) -> bool:
        """ delete all fluents

        Returns:
            bool: succeed
        """

        fluent_dto_list = self.get_all()

        for ele in fluent_dto_list:
            self.delete(ele)

        return True
