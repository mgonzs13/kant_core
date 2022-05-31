
from .test_dao_basic.test_action_dao import TestActionDao
from kant.kant_dao.dao_factory import (
    DaoFactoryMethod,
    DaoFamilies
)


class TestMongoActionDao(TestActionDao):

    DaoFactoryMethod.clear_dao_factory()
    DaoFactoryMethod(DaoFamilies.MONGO,
                     uri="mongodb://localhost:27017/kant_tests")


del(TestActionDao)
