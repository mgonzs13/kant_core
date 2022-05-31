
from .test_dao_basic.test_fluent_dao import TestPredicateDao
from kant.kant_dao.dao_factory import (
    DaoFactoryMethod,
    DaoFamilies
)


class TestMongoFluentteDao(TestPredicateDao):

    def setUp(self):
        super().setUp()
        dao_factory_method = DaoFactoryMethod()
        dao_factory = dao_factory_method.create_dao_factory(
            DaoFamilies.MONGO, uri="mongodb://localhost:27017/kant_tests")

        self.pddl_type_dao = dao_factory.create_type_dao()
        self.pddl_fluent_dao = dao_factory.create_fluent_dao()


del(TestPredicateDao)
