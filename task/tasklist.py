#!/usr/bin/python
# -*- coding:utf8 -*-

from .task import Task
from ..utils import check
from ..utils import TypeConstraint, SelfType, UnionType


class TaskEntryConstraint(TypeConstraint):
    task = UnionType(Task, None)
    task_id = int
    next = UnionType(SelfType, None)
    pre = UnionType(SelfType, None)
    time = int


@check(TaskEntryConstraint)
class TaskEntry(object):

    def __init__(self, task_id=-1, task=None, time=0,  pre=None, next=None):
        self.task = task
        self.task_id = task_id
        self.next = next
        self.pre = pre
        self.time = time


class TaskList(object):

    def __init__(self, delay):

        self.delay = delay
        self.lookup = dict()
        self._init_list()

    def _init_list(self):
        self.head = TaskEntry()
        self.head.next = self.head
        self.head.pre = self.head

    def add_task(self, time, task_name, task):
        cur = TaskEntry(task_name, task, time)
        tail = self.head.pre
        cur.pre = tail
        tail.next = cur
        cur.next = self.head
        self.head.pre = cur
        self.lookup[task_name] = cur

    def remove_task(self, task_name):

        if task_name not in self.lookup:
            raise Exception(
                "task_name : {} not exist".format(task_name))

        cur = self.lookup[task_name]
        pre = cur.pre
        next = cur.next
        pre.next = next
        next.pre = next
        del self.lookup[task_name]

    def get_tasks(self):
        return list(self.lookup.values())

    def done_once(self):
        self._init_list()
