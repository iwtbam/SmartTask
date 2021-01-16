from abc import abstractmethod, ABCMeta
import time
import os
import subprocess
from enum import Enum
from typing import List
from collections import Iterable


class TaskState(Enum):
    SUCCESS = 0
    WAIT = 1
    FAIL = 2


class TaskType(Enum):
    ONCE = 0
    REPEAT = 1


class TaskRuner(metaclass=ABCMeta):

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def check(self, *args, **kwargs):
        pass


class TaskRunCondition(metaclass=ABCMeta):

    @abstractmethod
    def check(self, *args, **kwargs):
        pass

    @abstractmethod
    def hint(self):
        pass


class TaskBasicDetail(object):

    def __init__(self, task_name, max_retry, conditions):
        self.task_name = task_name
        self.max_retry = max_retry
        self.task_state = TaskState.WAIT
        self.conditions = conditions

    @property
    def max_retry(self):
        return self.__max_retry

    @max_retry.setter
    def max_retry(self, val):
        if not isinstance(val, int):
            raise Exception("max retry must be int")
        self.__max_retry = val

    @property
    def conditions(self):
        return self.__conditions

    @conditions.setter
    def conditions(self, val):

        if val is None:
            self.__conditions = val
            return

        if not isinstance(val, Iterable):
            raise Exception("conditions must be Iterable or None")

        for condition in val:
            if not isinstance(condition, TaskRunCondition):
                raise Exception("single condition must be TaskRunCondition")
        self.__conditions = val


class Task(TaskRuner, TaskBasicDetail):
    pass
