from abc import abstractmethod, ABCMeta
import time
import os
import subprocess
from enum import Enum
from typing import List
from collections import Iterable
from .condition import TaskRunCondition
from ..utils import check, TypeConstraint, UnionType, NestedType


class TaskState(Enum):
    SUCCESS = 0
    WAIT = 1
    FAIL = 2


class TaskType(Enum):
    SUCCESS_RET = 0
    FIXED_RATE = 1


class TaskRuner(metaclass=ABCMeta):

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def check(self, *args, **kwargs):
        pass


class TaskConstraint(TypeConstraint):
    task_name = str
    max_retry = int
    task_type = TaskType
    task_state = TaskState
    run_times = int
    conditions = UnionType(None, NestedType(Iterable, True, TaskRunCondition))


@check(TaskConstraint)
class TaskDetail(object):

    def __init__(self, task_name, max_retry=1, task_type=TaskType.SUCCESS_RET, conditions=None):
        self.task_name = task_name
        self.max_retry = max_retry
        self.task_state = TaskState.WAIT
        self.task_type = task_type
        self.conditions = conditions
        self.run_times = 0


class Task(TaskRuner, TaskDetail):
    pass
