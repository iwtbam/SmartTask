from .timer import TimeWheelMananger
from .task import *
import threading
from queue import Queue


class Schedule(TimeWheelMananger):

    def __init__(self, min_interval, slots=(60, 60, 24)):
        TimeWheelMananger.__init__(self, min_interval, slots)
        self.is_tick = False
        self.task_queue = Queue()
        self.tick_thread = threading.Thread(target=self.__tick)

    def start(self):
        self.is_tick = True
        self.tick_thread.start()
        self.__execute()

    def stop(self):
        self.is_tick = False

    def __tick(self):
        while self.is_tick:
            tasks = self.tick()
            for task in tasks:
                self.task_queue.put(task)

    def __execute(self):
        while self.is_tick:
            task = self.task_queue.get()
            task.run()
