
from .test_dao_basic.test_type_dao import TestTypeDao
from kant.kant_dao.dao_factory import (
    DaoFactoryMethod,
    DaoFamilies
)


class TestMongoTypeDao(TestTypeDao):

    DaoFactoryMethod.clear_dao_factory()
    DaoFactoryMethod(DaoFamilies.MONGO,
                     uri="mongodb://localhost:27017/kant_tests")


del(TestTypeDao)
