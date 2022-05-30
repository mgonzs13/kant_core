# KANT (Knowledge mAnagemeNT)

This is a Python tool to manage PDDL-based knowledge. It is based on several software design patterns (DTO, DAO, Factory).

## Table of Contents

1. [Features](#features)
2. [Installation](#installation)
   - [MongoDB](#mongodb)
   - [Mongo Compass (Optional)](#mongo-compass-optional)
   - [KANT](#kant)
3. [Demos](#demos)

## Features

![](./images/diagram.png)

There are two DAO families implemented:

- `MONGO`: this is a DAO family that uses MongoDB to storage the PDDL knowledge. Besides, the Mongoengine Python library is used to access MongoDB.

PDDL elements (DTOs) that can be used are:

- types
- objects
- predicates
- propositions
- goals
- actions (and durative)

## Installation

### MongoDB

```shell
$ wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
$ sudo apt-get install gnupg
$ wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | sudo apt-key add -
$ echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | sudo tee /etc/apt/$ sources.list.d/mongodb-org-4.4.list
$ sudo apt-get update
$ sudo apt-get install -y mongodb-org
$ sudo systemctl start mongod
```

### Mongo Compass (Optional)

https://docs.mongodb.com/compass/master/install/

### KANT

```shell
$ git git@github.com:mgonzs13/kant_core.git
$ cd ~/kant_core
$ sudo python3 setup.py install
```

## Demos

```python
#!/usr/bin/env python3

from kant.kant_dao.dao_factory import (
    DaoFactoryMethod,
    DaoFamilies
)

from kant.kant_dto import (
    PddlTypeDto,
    PddlObjectDto,
    PddlPredicateDto,
    PddlPropositionDto,
    PddlConditionEffectDto,
    PddlActionDto
)

dao_factory_method = DaoFactoryMethod()
uri = "mongodb://localhost:27017/kant"
dao_family = DaoFamilies.MONGO
dao_factory = dao_factory_method.create_dao_factory(dao_family,
                                                    uri=uri)

# creating DAOs
pddl_type_dao = dao_factory.create_pddl_type_dao()
pddl_object_dao = dao_factory.create_pddl_object_dao()
pddl_predicate_dao = dao_factory.create_pddl_predicate_dao()
pddl_proposition_dao = dao_factory.create_pddl_proposition_dao()
pddl_action_dao = dao_factory.create_pddl_action_dao()

# types
robot_type = PddlTypeDto("robot")
wp_type = PddlTypeDto("wp")

# predicates
robot_at = PddlPredicateDto(
    "robot_at", [robot_type, wp_type])

# objects
rb1 = PddlObjectDto(robot_type, "rb1")
wp1 = PddlObjectDto(wp_type, "wp1")
wp2 = PddlObjectDto(wp_type, "wp2")

# propositions
pddl_proposition_dto = PddlPropositionDto(robot_at, [rb1, wp1])
pddl_goal_dto = PddlPropositionDto(robot_at, [rb1, wp2], is_goal=True)

# actions
r = PddlObjectDto(robot_type, "r")
s = PddlObjectDto(wp_type, "s")
d = PddlObjectDto(wp_type, "d")

condition_1 = PddlConditionEffectDto(robot_at,
                                     [r, s],
                                     time=PddlConditionEffectDto.AT_START)

effect_1 = PddlConditionEffectDto(robot_at,
                                  [r, s],
                                  time=PddlConditionEffectDto.AT_START,
                                  is_negative=True)

effect_2 = PddlConditionEffectDto(robot_at,
                                  [r, d],
                                  time=PddlConditionEffectDto.AT_END)

pddl_action_dto = PddlActionDto(
    "navigation", [r, s, d], [condition_1], [effect_1, effect_2])

# saving all
pddl_object_dao.save(rb1)
pddl_object_dao.save(wp1)
pddl_object_dao.save(wp2)

pddl_proposition_dao.save(pddl_proposition_dto)
pddl_proposition_dao.save(pddl_goal_dto)

pddl_action_dao.save(pddl_action_dto)

```
