import threading
from enum import Enum


class TaskStatus(Enum):
    IDLE = 'idle'
    RUNNING = 'running'
    CANCELED = 'canceled'
    FAILED = 'failed'
    COMPLETED = 'completed'
    

class Task(threading.Thread):
    def __init__(self, name, inputs, params, queue, notify_finished_callback):
        super(Task, self).__init__()
        self._name = name
        self._inputs = inputs
        self._params = params
        self._queue = queue
        self._status = TaskStatus.IDLE
        self._cancel_event = threading.Event()
        self._progress = 0
        self._notify_finished_callback = notify_finished_callback

    def name(self):
        return self._name
    
    def input(self, name):
        if name in self._inputs.keys():
            return self._inputs[name]
        return None
    
    def param(self, name, default=None):
        if name in self._params.keys():
            return self._params[name]
        return default
    
    def queue(self):
        return self._queue
    
    def status(self):
        return self._status

    def set_status(self, status):
        self._status = status

    def progress(self):
        return self._progress
    
    def set_progress(self, step, nr_steps):
        self._progress = int(((step + 1) / (nr_steps)) * 100)
        
    def run(self):
        try:
            self.set_status(TaskStatus.RUNNING)
            output = self.execute()
            if not self.is_canceled():
                self.queue().put(output)
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
        self._notify_finished_callback()