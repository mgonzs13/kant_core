
""" Mongo Dao Interface """

from abc import ABC, abstractmethod, abstractstaticmethod
from mongoengine import Document, disconnect, connect
from kant.kant_dto import Dto


class MongoDao(ABC):
    """ Mongo Dao Abstract Class """

    def __init__(self,
                 uri: str = "mongodb://localhost:27017/kant",
                 connect: bool = True
                 ) -> None:
        self.uri = uri

        if connect:
            self.connect()

    def connect(self) -> None:
        """ connect to current uri
        """

        disconnect()
        connect(host=self.uri)

    @property
    def uri(self) -> str:
        return self._uri

    @uri.setter
    def uri(self, uri: str) -> None:
        self._uri = uri

    @abstractmethod
    def _get_model(self, dto: Dto) -> Document:
        """ get the Mongoengine document corresponding to a give Dto

        Args:
            dto (Dto): Dto

        Returns:
            Document: Mongoengine document
        """

    @abstractmethod
    def _exist_in_mongo(dto: Dto) -> bool:
        """ check if Dto exists

        Args:
            dto (Dto): Dto

        Returns:
            bool: Dto exists?
        """

    @abstractstaticmethod
    def _model_to_dto(model: Document) -> Dto:
        """ convert a Mongoengine document into a Dto

        Args:
            model (Document): Mongoengine document

        Returns:
            Dto: Dto
        """

    @abstractstaticmethod
    def _dto_to_model(self, dto: Dto) -> Document:
        """ convert a Dto into a Mongoengine document

        Args:
            dto (Dto): Dto

        Returns:
            Document: Mongoengine document
        """
