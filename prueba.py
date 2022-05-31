from kant.kant_dao.dao_factory import (
    DaoFactoryMethod,
    DaoFamilies
)

dao_factory_method = DaoFactoryMethod(DaoFamilies.MONGO,
                                      uri="mongodb://localhost:27017/kant_tests")

print(DaoFactoryMethod.get_dao_factory())
