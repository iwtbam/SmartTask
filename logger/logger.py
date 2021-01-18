from functools import wraps
import logging


class Logger(object):
    def __init__(self, name, level=logging.DEBUG, format=None):
        if format is None:
            format = '%(asctime)s - %(name)s - %(lineno)d - %(levelname)s : %(message)s'
        self.name = name
        logging.basicConfig(level=level, format=format)

    def __call__(self, cls):
        setattr(cls, 'logger', logging.getLogger(self.name))
        return cls
