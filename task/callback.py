from abc import ABCMeta, abstractmethod
from enum import Enum
import threading


class TaskEvent(Enum):
    RUN_START = 0
    RUN_END = 1
    RUN_EXCEPTION = 2
    DONE = 3


class CallBack(metaclass=ABCMeta):

    def __init(self, sync=True):
        self.sync = sync

    @abstractmethod
    def done(self, *args, **kwargs):
        pass

    @abstractmethod
    def start_run(self, *args, **kwargs):
        pass

    @abstractmethod
    def end_run(self, *args, **kwargs):
        pass

    @abstractmethod
    def exception(self, *args, **kwargs):
        pass

    def dispatch_event(self, event, *args, **kwargs):

        target = None

        if event == TaskEvent.RUN_START:
            target = self.start_run

        if event == TaskEvent.RUN_END:
            target = self.end_run

        if event == TaskEvent.RUN_EXCEPTION:
            target = self.exception

        if event == TaskEvent.DONE:
            target = self.done

        if self.sync:
            sync_thread = threading.Thread(
                target=target, args=args, kwargs=kwargs)
            sync_thread.start()
        else:
            target(*args, **kwargs)
