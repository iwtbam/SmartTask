from croniter import croniter
from datetime import datetime


class CronTimer(object):

    def __init__(self, times, cron_express, base_time=None):
        self.times = times
        if not croniter.is_valid(cron_express):
            raise Exception("cron expression is not valid")
        self.__cron_express = cron_express
        if base_time is None:
            self.base_time = datetime.now()
        else:
            if not isinstance(base_time, datetime):
                raise Exception("base time must be datetime")
            self.base_time = base_time
        self.__pre_time = self.base_time
        self.cron_iter = croniter(self.__cron_express, self.base_time)

    def get_next(self):
        if self.times <= 0:
            return -1
        cur_time = self.cron_iter.get_next(datetime)
        diff = cur_time - self.__pre_time
        self.__pre_time = cur_time
        self.times -= 1
        return diff.total_seconds()
