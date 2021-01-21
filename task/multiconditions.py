from .condition import TaskRunCondition
from ..utils import default_logger
import os
import re


@default_logger
class NVIDIAGPUMemoryLimit(TaskRunCondition):

    NVIDIA_CMD = 'nvidia-smi --query-gpu=memory.total,memory.used,free.memory --format=csv'

    def __init__(self, limit, multi=False):
        self.limit = limit
        self.multi = multi
        self.ret = ""

    def check(self, *args, **kwargs):
        gpu_infos = self.get_gpu_info()

        for gpu_id, gpu_info in enumerate(gpu_infos):
            if gpu_info[2] > self.limit:
                self.ret = str(gpu_id)
                return True
        return False

    def get_gpu_info(self):
        with os.popen(self.NVIDIA_CMD, 'r') as rfile:
            lines = rfile.readlines()[1:]

            def search_func(line):
                res = re.findall(r'(\d+).+?(\d+).+?(\d+)', line)
                if len(res) == 0 or len(res[0]) < 3:
                    return None
                return list(map(lambda x: int(x), res[0]))

            return list(map(search_func, lines))

    def hint(self):
        return ""

    def args(self):
        return self.ret
