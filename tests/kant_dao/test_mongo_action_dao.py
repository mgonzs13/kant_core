
from .test_dao_basic.test_action_dao import TestActionDao
from kant.kant_dao.dao_factory import (
    DaoFactoryMethod,
    DaoFamilies
)


class TestMongoActionDao(TestActionDao):

    def setUp(self):
        super().setUp()

        dao_factory_method = DaoFactoryMethod()
        dao_factory = dao_factory_method.create_dao_factory(
            DaoFamilies.MONGO, uri="mongodb://localhost:27017/kant_tests")

        self.type_dao = dao_factory.create_type_dao()
        self.pdd_dao_predicate = dao_factory.create_fluent_dao()
        self.action_dao = dao_factory.create_action_dao()


del(TestActionDao)
