from .task import Task
from .task import TaskState
from .task import TaskDetail
import subprocess
import sys
from .task import *
from ..logger import Logger


@Logger(__name__)
class ShellTask(Task):

    def __init__(self, task_name, shell_command, log_file=None,  conditions=None, max_retry=1, task_type=TaskType.SUCCESS_RET):
        TaskDetail.__init__(
            self, task_name, max_retry, task_type, conditions)
        self.command = shell_command
        self.log_file = log_file

    def run(self, *args):

        if self.max_retry == 0:
            return TaskState.FAIL

        arguments = ' '.join(map(lambda x: str(x), args))
        run_command = '{} {}'.format(self.command, arguments)

        self.logger.info(run_command)

        if self.log_file is None:
            out_log = sys.stdout
            err_log = sys.stderr

        else:
            log_fd = open(self.log_file, 'a+')
            out_log = log_fd
            err_log = log_fd

        process = subprocess.Popen(
            run_command, shell=True, stdout=out_log, stderr=err_log)
        status_code = process.wait()
        if status_code == 0:
            return TaskState.SUCCESS
        self.max_retry -= 1

        if self.log_file is not None:
            log_fd.flush()
            log_fd.close()

        return TaskState.FAIL

    def check(self, *args, **kwargs):

        if self.conditions is None or len(self.conditions) == 0:
            return True, "no condition"

        for condition in self.conditions:
            if condition(*args, **kwargs) == False:
                return False, condition.hint()
        return True, None
