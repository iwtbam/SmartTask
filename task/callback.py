from abc import ABCMeta, abstractmethod
from enum import Enum


class TaskEvent(Enum):
    START_RUN = 0
    END_RUN = 1
    DONE = 2


class CallBack(metaclass=ABCMeta):

    def __init(self, sync=True):
        self.sync = sync

    @abstractmethod
    def done(self):
        pass

    @abstractmethod
    def start_run(self):
        pass

    @abstractmethod
    def end_run(self):
        pass

    def dispatch_event(self, event):

        if event == TaskEvent.START_RUN:
            self.start_run()

        if event == TaskEvent.END_RUN:
            self.end_run()

        if event == TaskEvent.DONE:
            self.done()
