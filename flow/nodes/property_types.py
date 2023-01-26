from typing import List, Type


class PropertyType(object):
    """
    This is a base class for property types
    """

    name: str

    code: str

    def accepts(self) -> List[Type["PropertyType"]]:
        """
        This method returns a list of accepted types
        """
        raise NotImplementedError


class StringType(PropertyType):
    """
    This is a string type
    """

    name: str = "String"
    code: str = "string"

    def accepts(self) -> list[Type[PropertyType]]:
        return [StringType, NumberType, BooleanType, ObjectType]


class NumberType(PropertyType):
    """
    This is an integer type
    """

    name: str = "Number"
    code: str = "number"

    def accepts(self) -> list[Type[PropertyType]]:
        return [NumberType]


class BooleanType(PropertyType):
    """
    This is a boolean type
    """

    name: str = "Boolean"
    code: str = "boolean"

    def accepts(self) -> list[Type[PropertyType]]:
        return [BooleanType]


class ObjectType(PropertyType):
    """
    This is an object type
    """

    name: str = "Object"
    code: str = "object"

    def accepts(self) -> list[Type[PropertyType]]:
        return [ObjectType]


PROPERTY_TYPE_CHOICES = list(map(lambda x: (x.name, x.code), PropertyType.__subclasses__()))
