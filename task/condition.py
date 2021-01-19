from abc import ABCMeta, abstractmethod


class TaskRunCondition(metaclass=ABCMeta):

    @abstractmethod
    def check(self, *args, **kwargs):
        pass

    @abstractmethod
    def hint(self):
        pass

    def args(self):
        return ""
