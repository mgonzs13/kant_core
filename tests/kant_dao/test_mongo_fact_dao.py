
from .test_dao_basic.test_fact_dao import TestFactDao
from kant.kant_dao.dao_factory import (
    DaoFactoryMethod,
    DaoFamilies
)


class TestMongoFactDao(TestFactDao):

    DaoFactoryMethod.clear_dao_factory()
    DaoFactoryMethod(DaoFamilies.MONGO,
                     uri="mongodb://localhost:27017/kant_tests")


del(TestFactDao)
