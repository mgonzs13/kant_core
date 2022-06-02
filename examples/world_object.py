
from kant.kant_dto import *
from kant.kant_dao import DaoFactoryMethod

from location import Location, location


# domain
world_object = TypeDto("world_object")
at = FluentDto("at", [world_object, location])


class WorldObject:

    def __init__(self, name: str, save: bool = True) -> None:

        self._world_object_object: ObjectDto = ObjectDto(world_object, name)
        self._at_fact: FactDto = None

        if save:
            self.save()

    def __str__(self) -> str:

        string = "world_object: " + self.name

        if not self.at is None:
            string += "\n\t" + at.get_name() + ": " + self.at.name

        return string

    @property
    def name(self) -> float:
        return self._world_object_object.get_name()

    @name.setter
    def name(self, name: str) -> None:
        self._world_object_object.set_name(name)
        self.save()

    @property
    def at(self) -> Location:
        if self._at_fact is None:
            return None

        return Location.get(self._at_fact.get_objects()[1].get_name())

    @at.setter
    def at(self, location: Location) -> None:

        dao_factory = DaoFactoryMethod.get_dao_factory()
        object_dao = dao_factory.create_object_dao()
        fact_dao = dao_factory.create_fact_dao()

        # destroy old fact
        if not self._at_fact is None:
            fact_dao.delete(self._at_fact)

        # create new fact
        location_object = object_dao.get(location.name)
        self._at_fact = FactDto(
            at, [self._world_object_object, location_object])
        self.save()

    # save & get
    def save(self) -> bool:

        dao_factory = DaoFactoryMethod.get_dao_factory()
        object_dao = dao_factory.create_object_dao()

        if not object_dao.save(self._world_object_object):
            return False

        if self._at_fact:

            fact_dao = dao_factory.create_fact_dao()

            if not fact_dao.save(self._at_fact):
                return False

        return True

    @staticmethod
    def get(name: str) -> "WorldObject":
        dao_factory = DaoFactoryMethod.get_dao_factory()
        fact_dao = dao_factory.create_fact_dao()
        object_dao = dao_factory.create_object_dao()

        world_object = WorldObject(name)

        # search for world_objects facts
        world_object_object = object_dao.get(name)

        at_fact = Location._find_fact(
            world_object_object, fact_dao.get_by_fluent(at.get_name()))

        if at_fact:
            world_object.at = Location.get(
                at_fact.get_objects()[1].get_name())

        return world_object
