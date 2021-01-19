from .. import task
import time
from queue import PriorityQueue
import threading
import random
from ..logger import *


class TimeWheel(object):

    def __init__(self, slot_num, interval, next=None):
        self.current_pos = 0
        self.slot_num = slot_num
        self.task_buckets = [task.TaskList(i) for i in range(self.slot_num)]
        self.next_time_wheel = next
        self.interval = interval

    @property
    def current_pos(self):
        return self.__current_pos

    @current_pos.setter
    def current_pos(self, val):
        if not isinstance(val, int):
            raise Exception("current pos must be int")
        self.__current_pos = val


@default_logger
class TimeWheelMananger(object):

    def __init__(self, min_interval, slots=None):
        self.slots = slots
        self.level = len(slots)
        self.min_interval = min_interval
        self.address_lookup = dict()
        self.aux_ticker = PriorityQueue()
        self.current_tick_times = 0
        self.__init_time_wheels(self.slots)
        self.task_id = 0

    def __init_time_wheels(self, slots):
        tick_times = 1
        self.time_wheels = []
        for slot in slots:
            self.time_wheels.append(TimeWheel(slot, tick_times))
            tick_times *= slot

        self.max_tick_times = tick_times
        self.time_wheel_num = len(self.time_wheels)
        for i in range(self.time_wheel_num - 1):
            self.time_wheels[i].next_time_wheel = self.time_wheels[i + 1]

    def add_task(self, delay, task):
        task_id = self.task_id
        delay = delay % self.max_tick_times
        time_wheel_no, offset = self.__index(delay)
        slot_no = (self.time_wheels[time_wheel_no].current_pos +
                   offset) % self.time_wheels[time_wheel_no].slot_num
        self.aux_ticker.put(delay + self.current_tick_times)
        task_list = self.__get_task_list(time_wheel_no, slot_no)
        task_list.add_task(delay + self.current_tick_times, task_id, task)
        self.address_lookup[task_id] = (time_wheel_no, slot_no)
        self.task_id += 1
        return task_id

    def remove_task(self, task_id):
        time_wheel_no, slot_no = self.address_lookup[task_id]
        task_list = self.__get_task_list(time_wheel_no, slot_no)
        task_list.remove_task(task_id)
        del self.address_lookup[task_id]

    def get_current_pos(self):
        pos = []
        for i in range(len(self.time_wheels)):
            pos.append(self.time_wheels[i].current_pos)
        return pos[::-1]

    def tick(self):

        if not self.aux_ticker.empty():
            delay = self.aux_ticker.get()
            self.logger.info('delay {}, current tick times {}'.format(
                delay, self.current_tick_times))
            wait_tick_times = delay - self.current_tick_times
            time.sleep(wait_tick_times * self.min_interval)
            self.current_tick_times = delay
            tasks = self.__time_wheel_tick(0, wait_tick_times)
        else:
            time.sleep(self.min_interval)
            self.current_tick_times += 1
            tasks = self.__time_wheel_tick(0, 1)

        return self.__dispatch(tasks)

    def __time_wheel_tick(self, time_wheel_no, num):

        cur_time_wheel = self.time_wheels[time_wheel_no]
        cur_slot_num = cur_time_wheel.slot_num
        cur_task_buckets = cur_time_wheel.task_buckets

        cur_pos = cur_time_wheel.current_pos + num
        cur_time_wheel.current_pos = cur_pos % cur_slot_num
        carry = cur_pos // cur_time_wheel.slot_num
        cur_pos = cur_time_wheel.current_pos

        task_list = cur_task_buckets[cur_pos]
        task_entrys = task_list.get_tasks()

        for entry in task_entrys:
            self.remove_task(entry.task_id)

        if carry > 0 and time_wheel_no + 1 < self.time_wheel_num:
            task_entrys.extend(self.__time_wheel_tick(
                time_wheel_no + 1,  carry))

        return task_entrys

    def __dispatch(self, task_entrys):
        expriedTask = []
        for entry in task_entrys:
            if entry.time <= self.current_tick_times:
                expriedTask.append(entry.task)
            else:
                self.add_task(
                    entry.time - self.current_tick_times, entry.task)
        return expriedTask

    def __index(self, delay):
        num = delay
        for i in range(self.level):
            if num < self.slots[i]:
                return i, num
            num = num // self.slots[i]
        return self.level - 1, self.slots[self.level - 1] - 1

    def __get_task_list(self, time_wheel_no, slot_no):
        time_wheel = self.time_wheels[time_wheel_no]
        return time_wheel.task_buckets[slot_no]
