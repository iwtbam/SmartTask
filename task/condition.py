from abc import ABCMeta, abstractmethod


class NoFit(object):

    def __init__(self, hint):
        self.hint = hint


class TaskRunCondition(metaclass=ABCMeta):

    class NoFit(object):
        pass

    @abstractmethod
    def check(self, *args, **kwargs):
        pass

    def hint(self):
        return "No Fit Condition : {}".format(type(self).__name__)

