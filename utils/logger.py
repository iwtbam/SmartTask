from functools import wraps
import logging


class Logger(object):
    def __init__(self, name=None, level=logging.DEBUG, format=None):
        if format is None:
            format = '%(asctime)s - %(filename)s - %(name)s - %(lineno)d - %(levelname)s : %(message)s'
        self.name = name
        logging.basicConfig(level=level, format=format)

    # @wraps
    def __call__(self, cls):
        name = self.name
        if name is None:
            name = cls.__name__
        setattr(cls, 'logger', logging.getLogger(name))
        return cls


default_logger = Logger()
