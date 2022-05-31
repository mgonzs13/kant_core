
""" Mongo Dao Facory """

from mongoengine import disconnect, connect

from kant.kant_dao.mongo_dao import (
    MongoTypeDao,
    MongoObjectDao,
    MongoFluentDao,
    MongoFactDao,
    MongoActionDao
)

from kant.kant_dao.dao_factory.dao_factories.dao_factory import DaoFactory


class MongoDaoFactory(DaoFactory):
    """ Mongo Dao Facory Class """

    def __init__(self, uri: str = "mongodb://localhost:27017/kant") -> None:
        self.set_uri(uri)
        self.connect()

    def connect(self):
        """ connect to current uri
        """

        disconnect()
        connect(host=self._uri)

    def get_uri(self) -> str:
        """ uri getter

        Returns:
            str: uri str
        """

        return self._uri

    def set_uri(self, uri: str):
        """ uri setter

        Args:
            uri (str): uri str
        """

        self._uri = uri

    def create_type_dao(self) -> MongoTypeDao:
        """ create a mongo dao type object

        Returns:
            MongoTypeDao: mongoengine dao for type
        """

        return MongoTypeDao(uri=self._uri, connect=False)

    def create_fluent_dao(self) -> MongoFluentDao:
        """ create a mongo dao fluent object

        Returns:
            MongoFluentDao: mongoengine dao for fluent
        """

        return MongoFluentDao(uri=self._uri, connect=False)

    def create_action_dao(self) -> MongoActionDao:
        """ create a mongo dao action object

        Returns:
            MongoActionDao: mongoengine dao for action
        """

        return MongoActionDao(uri=self._uri, connect=False)

    def create_object_dao(self) -> MongoObjectDao:
        """ create a mongo dao object object

        Args:
            uri (str, optional): Mongo uri. Defaults to None.

        Returns:
            MongoObjectDao: mongoengine dao for object
        """

        return MongoObjectDao(uri=self._uri, connect=False)

    def create_fact_dao(self) -> MongoFactDao:
        """ create a mongo dao fact object

        Returns:
            MongoFactDao: mongoengine dao for fact
        """

        return MongoFactDao(uri=self._uri, connect=False)
