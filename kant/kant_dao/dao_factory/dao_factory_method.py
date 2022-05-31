
""" Dao Factory of Factories """

from kant.kant_dao.dao_factory.dao_families import DaoFamilies

from kant.kant_dao.dao_factory.dao_factories import (
    DaoFactory,
    MongoDaoFactory
)


class DaoFactoryMethod:
    """ Dao Factory of Factories Class """

    __shared_dao_factory: DaoFactory = None

    def __init__(self, family: int, **kwargs):

        if not DaoFactoryMethod.__shared_dao_factory is None:
            raise Exception("This class is a singleton")
        else:

            self.__families_to_factory = {
                DaoFamilies.MONGO: MongoDaoFactory
            }

            args_dict = {}

            dao_factory = self.__families_to_factory[family]
            init_args = list(dao_factory.__init__.__code__.co_varnames)

            for key, value in kwargs.items():
                if key in init_args:
                    args_dict[key] = value

            DaoFactoryMethod.__shared_dao_factory = dao_factory(**args_dict)

    @staticmethod
    def get_dao_factory() -> DaoFactory:
        """ Static Access Method
            get the dao factory created

        Returns:
            DaoFactory: dao factory
        """

        if DaoFactoryMethod.__shared_dao_factory is None:
            raise Exception("You must instanciate DaoFactoryMethod first")

        return DaoFactoryMethod.__shared_dao_factory

    @staticmethod
    def clear_dao_factory() -> None:
        """ 
            Static Access Method
            clear the dao factory
        """

        DaoFactoryMethod.__shared_dao_factory = None
