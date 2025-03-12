import uuid
import datetime
import threading

from enum import Enum

from ..managers.logmanager import LogManager

LOG = LogManager()


class TaskStatus(Enum):
    IDLE = 'idle'
    RUNNING = 'running'
    CANCELED = 'canceled'
    FAILED = 'failed'
    COMPLETED = 'completed'
    

class Task(threading.Thread):
    def __init__(self, input_files_dict, output_dir_dict, params, notify_finished_callback):
        super(Task, self).__init__()
        self._id = str(uuid.uuid4())
        self._name = self.__class__.__name__
        self._input_files_dict = input_files_dict
        self._output_dir_dict = output_dir_dict
        self._params = params
        self._status = TaskStatus.IDLE
        self._cancel_event = threading.Event()
        self._progress = 0
        self._notify_finished_callback = notify_finished_callback
        self._created = datetime.datetime.now()

    def id(self):
        return self._id

    def name(self):
        return self._name
    
    def input_files_dict(self):
        return self._input_files_dict
    
    def input_files(self, name):
        if name in self._input_files_dict.keys():
            return self._input_files_dict[name]
        return None
    
    def output_dir(self, name):
        if name in self._output_dir_dict.keys():
            return self._output_dir_dict[name]
        return None
    
    def param(self, name, default=None):
        if name in self._params.keys():
            return self._params[name]
        return default
    
    def status(self):
        return self._status.value

    def set_status(self, status, message=None):
        self._status = status
        self.log_info(f'status = {self._status.value} ({message})')

    def progress(self):
        return self._progress
    
    def set_progress(self, step, nr_steps):
        self._progress = int(((step + 1) / (nr_steps)) * 100)
        self.log_info(f'progress = {self._progress}')

    def created(self):
        return self._created
    
    def run(self):
        try:
            self.set_status(TaskStatus.RUNNING)
            self.execute()
            if not self.is_canceled():
                # self.queue().put(output)
                self.notify_finished()
                self.set_status(TaskStatus.COMPLETED)
        except Exception as e:
            self.set_status(TaskStatus.FAILED, str(e))

    def execute(self):
        raise NotImplementedError('Must be implemented in child class')

    def is_canceled(self):
        return self._cancel_event.is_set()
    
    def cancel(self):
        self._cancel_event.set()
        self.set_status(TaskStatus.CANCELED)

    def notify_finished(self):
        self._notify_finished_callback(self.id())

    # LOGGING

    def log_info(self, message):
        LOG.info(f'{self.__class__.__name__}: {message}')

    def log_warning(self, message):
        LOG.warning(f'{self.__class__.__name__}: {message}')

    def log_error(self, message):
        LOG.error(f'{self.__class__.__name__}: {message}')