
from .test_dao_basic.test_object_dao import TestObjectDao
from kant.kant_dao.dao_factory import (
    DaoFactoryMethod,
    DaoFamilies
)


class TestMongoObjectDao(TestObjectDao):

    DaoFactoryMethod.clear_dao_factory()
    DaoFactoryMethod(DaoFamilies.MONGO,
                     uri="mongodb://localhost:27017/kant_tests")


del(TestObjectDao)
