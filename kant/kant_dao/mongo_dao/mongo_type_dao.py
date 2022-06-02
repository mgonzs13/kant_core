
""" Mongo Type Dao """

from typing import List

from kant.kant_dao.dao_interface import TypeDao
from kant.kant_dao.mongo_dao import MongoDao

from kant.kant_dao.mongo_dao.mongo_models import TypeModel

from kant.kant_dto import TypeDto


class MongoTypeDao(TypeDao, MongoDao):
    """ Mongo Type Dao Class """

    def __init__(self, uri: str = None, connect: bool = True) -> None:

        TypeDao.__init__(self)
        MongoDao.__init__(self, uri, connect)

    @staticmethod
    def _model_to_dto(type_model: TypeModel) -> TypeDto:
        """ convert a Mongoengine type document into a TypeDto

        Args:
            type_model (TypeModel): Mongoengine type document

        Returns:
            TypeDto: TypeDto
        """

        type_dto = TypeDto(type_model.name)

        if type_model.father:
            type_dto.father = MongoTypeDao._model_to_dto(type_model.father)

        return type_dto

    @staticmethod
    def _dto_to_model(type_dto: TypeDto) -> TypeModel:
        """ convert a TypeDto into a Mongoengine type document

        Args:
            type_dto (TypeDto): TypeDto

        Returns:
            Document: Mongoengine type document
        """

        type_model = TypeModel()
        type_model.name = type_dto.name

        if type_dto.father:
            type_model.father = MongoTypeDao._dto_to_model(
                type_dto.father)

        return type_model

    def _exist_in_mongo(self, type_dto: TypeDto) -> bool:
        """ check if TypeDto exists

        Args:
            type_dto (TypeDto): TypeDto

        Returns:
            bool: TypeDto exists?
        """

        if self._get_model(type_dto):
            return True
        return False

    def _get_model(self, type_dto: TypeDto) -> TypeModel:
        """ get the Mongoengine type document corresponding to a give TypeDto

        Args:
            type_dto (TypeDto): TypeDto

        Returns:
            Document: Mongoengine type document
        """

        type_model = TypeModel.objects(name=type_dto.name)

        if not type_model:
            return None

        return type_model[0]

    def get(self, type_name: str) -> TypeDto:
        """ get a TypeDto with a given type name
            return None if there is no with that type name

        Args:
            type_name (str): type name

        Returns:
            TypeDto: TypeDto of the type name
        """

        type_model = TypeModel.objects(name=type_name)

        if type_model:
            type_model = type_model[0]
            return MongoTypeDao._model_to_dto(type_model)

        return None

    def get_all(self) -> List[TypeDto]:
        """ get all TypeDto

        Returns:
            List[TypeDto]: list of all TypeDto
        """

        type_model = TypeModel.objects.order_by("name")
        type_dto_list = []

        for ele in type_model:
            type_dto = MongoTypeDao._model_to_dto(ele)
            type_dto_list.append(type_dto)

        return type_dto_list

    def _save(self, type_dto: TypeDto) -> bool:
        """ save a TypeDto
            if the TypeDto is already saved return False, else return True

        Args:
            type_dto (TypeDto): TypeDto to save

        Returns:
            bool: succeed
        """

        if self._exist_in_mongo(type_dto):
            return False

        # propagating saving
        if type_dto.father:
            if not self.save(type_dto.father):
                return False

        # saving
        type_model = MongoTypeDao._dto_to_model(type_dto)
        type_model.save(force_insert=True)
        return True

    def _update(self, type_dto: TypeDto) -> bool:
        """ update a TypeDto
            if the TypeDto is not saved return False, else return True

        Args:
            type_dto (TypeDto): TypeDto to update

        Returns:
            bool: succeed
        """

        type_model = self._get_model(type_dto)

        # check if type exists
        if type_model:

            # propagating saving
            if type_dto.father:
                if not self.save(type_dto.father):
                    return False

            # updating
            type_model.name = type_dto.name
            type_model.save()
            return True

        return False

    def save(self, type_dto: TypeDto) -> bool:
        """ save or update a TypeDto
            if the TypeDto is not saved it will be saved, else it will be updated

        Args:
            type_dto (TypeDto): TypeDto to save or update

        Returns:
            bool: succeed
        """

        if self._exist_in_mongo(type_dto):
            return self._update(type_dto)

        return self._save(type_dto)

    def delete(self, type_dto: TypeDto) -> bool:
        """ delete a TypeDto
            if the TypeDto is not saved return False, else return True

        Args:
            type_dto (TypeDto): TypeDto to delete

        Returns:
            bool: succeed
        """

        type_model = self._get_model(type_dto)

        # check if type exists
        if type_model:
            type_model.delete()

            # delete childs
            child_models = TypeModel.objects(
                father=type_dto.name)

            for child in child_models:
                child.delete()

            return True

        return False

    def delete_all(self) -> bool:
        """ delete all types

        Returns:
            bool: succeed
        """

        type_dto_list = self.get_all()

        for ele in type_dto_list:
            self.delete(ele)

        return True
