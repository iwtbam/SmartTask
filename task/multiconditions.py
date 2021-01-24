from .condition import TaskRunCondition, NoFit
from ..utils import default_logger
import os
import re


@default_logger
class NVIDIAGPUMemoryLimit(TaskRunCondition):

    NVIDIA_CMD = 'nvidia-smi --query-gpu=memory.free --format=csv'

    def __init__(self, limit, multi=False):
        self.limit = limit
        self.multi = multi
        self.ret = ""

    def check(self, *args, **kwargs):
        gpu_infos = self.get_gpu_info()
        for gpu_id, free in enumerate(gpu_infos):
            self.logger.info(free)
            if free > self.limit:
                return gpu_id
        return NoFit(self.hint())

    def get_gpu_info(self):
        with os.popen(self.NVIDIA_CMD, 'r') as rfile:
            lines = rfile.readlines()[1:]

            def search_func(line):
                res = re.findall(r'(\d+)', line)
                if len(res) == 0 or len(res[0]) < 1:
                    return None
                return int(res[0])

            return list(map(search_func, lines))
