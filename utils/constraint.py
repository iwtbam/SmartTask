import re
from functools import wraps
from .logger import default_logger


class TypeConstraint(object):
    pass


class SelfType(object):
    pass


class UnionType(object):

    def __init__(self, *args):
        self.typelist = args

    def __str__(self):
        return '{}'.format(self.typelist)


@default_logger
class NestedType(object):

    def __init__(self, parent_type, is_same, *element_type):
        self.parent_type = parent_type
        self.element_type = element_type
        if len(self.element_type) < 1:
            raise Exception("element_type no less one type")
        self.is_same = is_same

        if self.is_same:
            self.element_type = self.element_type[0]


def __all_vars(cls):
    names = {}
    var_dict = vars(cls)
    for name in var_dict:
        if not re.match('^_', name):
            names[name] = var_dict[name]
    return names


def __validate(selftype, obj, cls):

    if obj == cls:
        return True

    if cls == SelfType:
        return isinstance(obj, selftype)

    if isinstance(cls, type) and isinstance(obj, cls):
        return True

    if isinstance(cls, UnionType):
        ret = False
        for type_args in cls.typelist:
            ret = ret or __validate(selftype, obj, type_args)
        return ret

    if isinstance(cls, NestedType):
        if not isinstance(obj, cls.parent_type):
            return False
        ret = True
        if cls.is_same == True:
            for e in obj:
                ret = ret and __validate(selftype, e, cls.element_type)
        else:
            min_validate_len = min(len(obj), len(cls.element_type))
            for i in range(min_validate_len):
                ret = ret and __validate(selftype, obj[i], cls.element_type[i])
        return True
    return False


def check(constraint):

    def setattr(self, name, val):
        var_dict = __all_vars(constraint)
        if name in var_dict:
            if not __validate(type(self), val, var_dict[name]):
                raise Exception('{} must be {}'.format(name, var_dict[name]))
        self.__dict__[name] = val

    def wrapper(cls):
        cls.__setattr__ = setattr
        return cls

    return wrapper
