
from .test_dao_basic.test_fluent_dao import TestPredicateDao
from kant.kant_dao.dao_factory import (
    DaoFactoryMethod,
    DaoFamilies
)


class TestMongoFluentteDao(TestPredicateDao):

    DaoFactoryMethod.clear_dao_factory()
    DaoFactoryMethod(DaoFamilies.MONGO,
                     uri="mongodb://localhost:27017/kant_tests")


del(TestPredicateDao)
