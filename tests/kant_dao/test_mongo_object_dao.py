
from .test_dao_basic.test_object_dao import TestObjectDao
from kant.kant_dao.dao_factory import (
    DaoFactoryMethod,
    DaoFamilies
)


class TestMongoObjectDao(TestObjectDao):

    def setUp(self):
        super().setUp()

        dao_factory_method = DaoFactoryMethod()
        dao_factory = dao_factory_method.create_dao_factory(
            DaoFamilies.MONGO, uri="mongodb://localhost:27017/kant_tests")

        self.object_dao = dao_factory.create_object_dao()
        self.type_dao = dao_factory.create_type_dao()


del(TestObjectDao)
