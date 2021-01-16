#!/usr/bin/python
# -*- coding:utf8 -*-

from .task import Task
from .shell_task import ShellTask


class TaskEntry(object):

    def __init__(self, task_id=-1, task=None, time=0,  pre=None, next=None):
        self.task = task
        self.task_id = task_id
        self.next = next
        self.pre = pre
        self.time = time

    @property
    def task(self):
        return self.__task

    @task.setter
    def task(self, val):
        if val is not None and not isinstance(val, Task):
            raise Exception("task : {} not be Task or None".format(val))
        self.__task = val

    @property
    def pre(self):
        return self.__pre

    @pre.setter
    def pre(self, val):
        if val is not None and not isinstance(val, TaskEntry):
            raise Exception("type of pre must be TaskEntry")
        self.__pre = val

    @property
    def next(self):
        return self.__next

    @next.setter
    def next(self, val):
        if val is not None and not isinstance(val, TaskEntry):
            raise Exception("type of next must be TaskEntry")
        self.__next = val

    @property
    def tick(self):
        return self.__tick

    @tick.setter
    def tick(self, val):
        if not (isinstance(val, int) or isinstance(val, int)):
            raise Exception("tick must be a number")
        self.__tick = val


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
