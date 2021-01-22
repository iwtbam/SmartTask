from .timer import TimeWheelManager
from .timer import CronTimer
from .task import TaskType, TaskState, TaskEvent, NoFit
import threading
from queue import Queue
from .utils import default_logger
from .utils import check, TypeConstraint, UnionType, NestedType


class ScheduleConstraint(TypeConstraint):
    is_tick = bool
    task_queue = Queue
    crons = dict
    states = dict
    callbacks = dict


@check(ScheduleConstraint)
@default_logger
class Schedule(TimeWheelManager):

    def __init__(self, min_interval, slots=(60, 60, 24)):
        TimeWheelManager.__init__(self, min_interval, slots)
        self.is_tick = False
        self.task_queue = Queue()
        self.tick_thread = threading.Thread(target=self.__tick)
        self.crons = dict()
        self.states = dict()
        self.callbacks = dict()
        self.__lock = threading.Lock()

    def start(self):
        self.is_tick = True
        self.tick_thread.start()
        self.__execute()

    def schedule(self, cron_express, run_times, task, callback=None):
        cron_timers = CronTimer(run_times, cron_express)
        self.crons[task] = cron_timers
        if callback is not None:
            self.callbacks[task] = callback
        self.__produce_task(task)

    def __produce_task(self, task):
        if task not in self.crons:
            return None
        delay_time = self.crons[task].get_next()
        if delay_time <= 0:
            self.__done(task)
            return None
        delay_tick = int(delay_time // self.min_interval)
        if delay_tick < 1:
            delay_tick = 1
        return self.add_task(delay_tick, task)

    def __done(self, task, *args, **kwargs):
        if task in self.crons:
            del self.crons[task]
        self.__notify_callback(task, TaskEvent.DONE, *args, **kwargs)

    def stop(self):
        self.is_tick = False

    def __tick(self):
        while self.is_tick:
            tasks = self.tick()
            for task in tasks:
                self.task_queue.put(task)

    def __notify_callback(self, task, event, *args, **kwargs):
        if task not in self.callbacks:
            return
        callback = self.callbacks[task]
        callback.dispatch_event(event, task, *args, **kwargs)

    def __execute(self):
        while self.is_tick:
            try:
                task = self.task_queue.get()
                status_code = TaskState.WAIT
                self.__notify_callback(task, TaskEvent.RUN_START)
                fit = True
                try:
                    check_res = task.check()
                    fit = not isinstance(check_res, NoFit)
                    if fit:
                        status_code = task.run(*check_res)
                    self.logger.info('{} {}'.format(fit,  task.task_name))
                except Exception as e:
                    self.logger.error(e)
                    self.__notify_callback(task, TaskEvent.RUN_EXCEPTION, e)
                finally:
                    if fit:
                        self.__notify_callback(task, TaskEvent.RUN_END)
                    else:
                        self.__notify_callback(task, TaskEvent.RUN_NO_FIT)
                    if task.task_type == TaskType.SUCCESS_RET and status_code == TaskState.SUCCESS:
                        self.__done(task)
            except Exception as e:
                self.logger.error("execute exception {}".format(e))
            finally:
                self.__produce_task(task)
