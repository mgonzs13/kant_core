
from .test_dao_basic.test_fact_dao import TestFactDao
from kant.kant_dao.dao_factory import (
    DaoFactoryMethod,
    DaoFamilies
)


class TestMongoPddlPropositionDao(TestFactDao):

    def setUp(self):
        super().setUp()
        dao_factory_method = DaoFactoryMethod()
        dao_factory = dao_factory_method.create_dao_factory(
            DaoFamilies.MONGO, uri="mongodb://localhost:27017/kant_tests")

        self.object_dao = dao_factory.create_object_dao()
        self.type_dao = dao_factory.create_type_dao()
        self.pdd_dao_fluent = dao_factory.create_fluent_dao()
        self.fact_dao = dao_factory.create_fact_dao()


del(TestFactDao)
