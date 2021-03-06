from abc import ABCMeta, abstractmethod
from enum import Enum
import threading


class TaskEvent(Enum):
    RUN_START = 0
    RUN_NO_FIT = 1
    RUN_END = 2
    RUN_EXCEPTION = 3
    DONE = 4


class CallBack(metaclass=ABCMeta):

    def __init(self, sync=True):
        self.sync = sync

    @abstractmethod
    def done(self, *args, **kwargs):
        pass

    @abstractmethod
    def start(self, *args, **kwargs):
        pass

    @abstractmethod
    def end(self, *args, **kwargs):
        pass

    @abstractmethod
    def no_fit(self, *args, **kwargs):
        pass

    @abstractmethod
    def exception(self, *args, **kwargs):
        pass

    def dispatch_event(self, event, *args, **kwargs):

        target = None

        if event == TaskEvent.RUN_START:
            target = self.start

        if event == TaskEvent.RUN_END:
            target = self.end

        if event == TaskEvent.RUN_EXCEPTION:
            target = self.exception

        if event == TaskEvent.DONE:
            target = self.done

        if event == TaskEvent.RUN_NO_FIT:
            target = self.no_fit

        if self.sync:
            sync_thread = threading.Thread(
                target=target, args=args, kwargs=kwargs)
            sync_thread.start()
        else:
            target(*args, **kwargs)
