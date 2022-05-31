
from kant.kant_dao import (
    DaoFactoryMethod,
    DaoFamilies
)

from location import Location

dao_factory_method = DaoFactoryMethod()
uri = "mongodb://localhost:27017/kant"
dao_family = DaoFamilies.MONGO
dao_factory = dao_factory_method.create_dao_factory(dao_family,
                                                    uri=uri)

wp1 = Location("wp1", 1.0, 2.5, 0.0, 0.0, 0.0, 0.0, 1.0)
wp1.save(dao_factory)

wp1 = Location.get("wp1", dao_factory)
print(wp1)
