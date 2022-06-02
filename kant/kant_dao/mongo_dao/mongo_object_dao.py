
""" Mongo Object Dao """

from typing import List

from kant.kant_dao.dao_interface import ObjectDao
from kant.kant_dao.mongo_dao import (
    MongoDao,
    MongoTypeDao
)

from kant.kant_dao.mongo_dao.mongo_models import ObjectModel


from kant.kant_dto import (
    ObjectDto,
    TypeDto
)


class MongoObjectDao(ObjectDao, MongoDao):
    """ Mongo Object Dao Class """

    def __init__(self, uri: str = None, connect: bool = True) -> None:

        ObjectDao.__init__(self)
        MongoDao.__init__(self, uri, connect)

        self._me_type_dao = MongoTypeDao(uri, connect=False)

    @staticmethod
    def _model_to_dto(object_model: ObjectModel) -> ObjectDto:
        """ convert a Mongoengine object document into a ObjectDto

        Args:
            object_model (ObjectModel): Mongoengine object document

        Returns:
            ObjectDto: ObjectDto
        """

        type_dto = MongoTypeDao._model_to_dto(object_model.type)

        object_dto = ObjectDto(type_dto,
                               object_model.name)

        return object_dto

    @staticmethod
    def _dto_to_model(object_dto: ObjectDto) -> ObjectModel:
        """ convert a ObjectDto into a Mongoengine object document

        Args:
            object_dto (ObjectDto): ObjectDto

        Returns:
            Document: Mongoengine object document
        """

        type_model = MongoTypeDao._dto_to_model(
            object_dto.type)

        object_model = ObjectModel()

        object_model.name = object_dto.name

        object_model.type = type_model

        return object_model

    def _exist_in_mongo(self, object_dto: ObjectDto) -> bool:
        """ check if ObjectDto exists

        Args:
            object_dto (ObjectDto): ObjectDto

        Returns:
            bool: ObjectDto exists?
        """

        if self._get_model(object_dto):
            return True

        return False

    def _get_model(self, object_dto: ObjectDto) -> ObjectModel:
        """ get the Mongoengine object document corresponding to a give ObjectDto

        Args:
            object_dto (ObjectDto): ObjectDto

        Returns:
            Document: Mongoengine object document
        """

        object_model = ObjectModel.objects(name=object_dto.name)

        if not object_model:
            return None

        return object_model[0]

    def get(self, object_name: str) -> ObjectDto:
        """ get a ObjectDto with a given object name
            return None if there is no with that object name

        Args:
            object_name (str): object name

        Returns:
            ObjectDto: ObjectDto of the object name
        """

        object_model = ObjectModel.objects(name=object_name)

        # check if object exists
        if object_model:
            object_model = object_model[0]
            object_dto = MongoObjectDao._model_to_dto(
                object_model)
            return object_dto

        return None

    def get_all(self) -> List[ObjectDto]:
        """ get all ObjectDto

        Returns:
            List[ObjectDto]: list of all ObjectDto
        """

        object_model = ObjectModel.objects.order_by("name")
        object_dto_list = []

        for ele in object_model:
            object_dto = MongoObjectDao._model_to_dto(ele)
            object_dto_list.append(object_dto)

        return object_dto_list

    def _save(self, object_dto: ObjectDto) -> bool:
        """ save a ObjectDto
            if the ObjectDto is already saved return False, else return True

        Args:
            object_dto (ObjectDto): ObjectDto to save

        Returns:
            bool: succeed
        """

        if self._exist_in_mongo(object_dto):
            return False

        object_model = MongoObjectDao._dto_to_model(
            object_dto)

        # propagating saving
        if not self._me_type_dao.save(object_dto.type):
            return False

        # saving
        object_model.save()
        return True

    def _update(self, object_dto: ObjectDto) -> bool:
        """ update a ObjectDto
            if the ObjectDto is not saved return False, else return True

        Args:
            object_dto (ObjectDto): ObjectDto to update

        Returns:
            bool: succeed
        """

        object_model = self._get_model(object_dto)

        # check if object exists
        if object_model:

            # propagating saving
            if not self._me_type_dao.save(object_dto.type):
                return False

            # updating
            new_object_model = MongoObjectDao._dto_to_model(
                object_dto)

            object_model.name = new_object_model.name
            object_model.type = new_object_model.type
            object_model.save()

            return True

        return False

    def save(self, object_dto: ObjectDto) -> bool:
        """ save or update a ObjectDto
            if the ObjectDto is not saved it will be saved, else it will be updated

        Args:
            object_dto (ObjectDto): ObjectDto to save or update

        Returns:
            bool: succeed
        """

        if self._exist_in_mongo(object_dto):
            return self._update(object_dto)

        return self._save(object_dto)

    def delete(self, object_dto: ObjectDto) -> bool:
        """ delete a ObjectDto
            if the ObjectDto is not saved return False, else return True

        Args:
            object_dto (ObjectDto): ObjectDto to delete

        Returns:
            bool: succeed
        """

        object_model = self._get_model(object_dto)

        # check if object exists
        if object_model:
            object_model.delete()
            return True

        return False

    def delete_all(self) -> bool:
        """ delete all objects

        Returns:
            bool: succeed
        """

        object_dto_list = self.get_all()

        for ele in object_dto_list:
            self.delete(ele)

        return True
