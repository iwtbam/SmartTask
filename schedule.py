from .timer import TimeWheelMananger
from .timer import CronTimer
from .task import *
import threading
from queue import Queue


class Schedule(TimeWheelMananger):

    def __init__(self, min_interval, slots=(60, 60, 24)):
        TimeWheelMananger.__init__(self, min_interval, slots)
        self.is_tick = False
        self.task_queue = Queue()
        self.tick_thread = threading.Thread(target=self.__tick)
        self.corns = dict()
        self.states = dict()
        self.callbacks = dict()

    def start(self):
        self.is_tick = True
        self.tick_thread.start()
        self.__execute()

    def schedule(self, cron_express, run_times, task, callback = None):
        cron_timers = CronTimer(run_times, cron_express)
        self.corns[task] = cron_timers
        self.__produce_task(task)

    def __produce_task(self, task):

        if task not in self.crons:
            return Non
        delay_time = self.corns[task].get_next()
        if delay_time <= 0:
            self.__done(task)
            return None
        delay_tick = int(delay_time // self.min_interval)
        return self.add_task(delay_tick, task)

    
    def __done(self, task):
        if task in self.crons:
            del self.cron[task]

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
            task_type = task.task_type
            status_code = TaskState.WAIT
            try:
                status_code = task.run()
            except Exception as e:
                print(e)
            finally:
                if task.task_type == TaskType.SUCCESS_RET and status_code = TaskState.SUCCESS:
                    self.__done(task)
                    continue
                self.__produce_task(task)
