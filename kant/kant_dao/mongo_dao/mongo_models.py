
""" Mongo models"""

from unittest.mock import mock_open
import mongoengine


class TypeModel(mongoengine.Document):
    """ type model """

    meta = {"collection": "type"}
    name = mongoengine.StringField(primary_key=True)
    father = mongoengine.ReferenceField(
        "self", reverse_delete_rule=mongoengine.CASCADE)


class ObjectModel(mongoengine.Document):
    """ object model """

    meta = {"collection": "object"}
    name = mongoengine.StringField(primary_key=True)
    type = mongoengine.ReferenceField(
        TypeModel, reverse_delete_rule=mongoengine.CASCADE)


class FluentModel(mongoengine.Document):
    """ predicate model """

    meta = {"collection": "fluent"}
    name = mongoengine.StringField(primary_key=True)
    is_numeric = mongoengine.BooleanField()
    types = mongoengine.ListField(
        mongoengine.ReferenceField(TypeModel,
                                   reverse_delete_rule=mongoengine.CASCADE))


class FactModel(mongoengine.Document):
    """ proposition model """

    meta = {"collection": "fact"}
    fluent = mongoengine.ReferenceField(
        FluentModel, reverse_delete_rule=mongoengine.CASCADE)
    arguments = mongoengine.ListField(
        mongoengine.ReferenceField(
            ObjectModel, reverse_delete_rule=mongoengine.CASCADE),
        db_field="objects")

    bool_value = mongoengine.BooleanField()
    numeric_value = mongoengine.DecimalField()

    is_goal = mongoengine.BooleanField()


class ParameterModel(mongoengine.EmbeddedDocument):
    """ parameter model """

    meta = {"collection": "parameter"}
    name = mongoengine.StringField()
    type = mongoengine.ReferenceField(TypeModel)


class ConditionEffectModel(mongoengine.EmbeddedDocument):
    """ contion/effect model """

    meta = {"collection": "condition_effect"}

    bool_value = mongoengine.BooleanField()
    numeric_value = mongoengine.DecimalField()

    condition_effect = mongoengine.StringField()
    time = mongoengine.StringField()

    fluent = mongoengine.ReferenceField(FluentModel)
    parameters = mongoengine.EmbeddedDocumentListField(ParameterModel)


class ActionModel(mongoengine.Document):
    """ action model """

    meta = {"collection": "action"}

    action_name = mongoengine.StringField(primary_key=True)
    duration = mongoengine.IntField(default=10)
    durative = mongoengine.BooleanField(default=True)

    parameters = mongoengine.EmbeddedDocumentListField(ParameterModel)

    _fluents = mongoengine.ListField(
        mongoengine.ReferenceField(FluentModel, reverse_delete_rule=mongoengine.CASCADE))

    conditions = mongoengine.EmbeddedDocumentListField(
        ConditionEffectModel)
    effects = mongoengine.EmbeddedDocumentListField(
        ConditionEffectModel)
