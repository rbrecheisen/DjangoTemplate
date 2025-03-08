import queue

from ..tasks.taskregistry import TASK_REGISTRY
from ..singleton import singleton


@singleton
class TaskManager:
    def __init__(self):
        self._tasks = {}

    # TASKS

    def tasks(self):
        return self._tasks
    
    def task_names(self):
        return TASK_REGISTRY.keys()
    
    def task_ok(self, task_info, inputs, params):
        for input_name in inputs.keys():
            if not input_name in task_info['inputs']:
                return False
        for param_name in params.keys():
            if not param_name in task_info['params']:
                return False
        return True

    def run_task(self, task_name, inputs, params, wait_to_finish=False):
        task_info = TASK_REGISTRY.get(task_name, None)
        if task_info:
            # Check if the inputs and parameters match the task's info
            if not self.task_ok(task_info, inputs, params):
                message = f'Provided inputs ({inputs.keys()}) and parameters ({params.keys()}) do not match {task_name}\' registry settings:\n'
                message += '[inputs]: {}\n'.format(task_info['inputs'])
                message += '[parameters]: {}'.format(task_info['params'])
                raise RuntimeError(message)
            # If task is already in the list, cancel and remove it
            if task_name in self.tasks().keys():
                self.cancel_task(task_name)
                self.remove_task(task_name)
            # Add the new task to the list with its own queue
            task_queue = queue.Queue()
            self.tasks()[task_name] = {
                'instance': task_info['class'](
                    inputs, params, task_queue, self.task_finished
                ),
                'queue': task_queue,
            }
            # Start the task and wait if necessary
            self.tasks()[task_name]['instance'].start()
            if wait_to_finish:
                self.tasks()[task_name]['instance'].join()

    def cancel_task(self, task_name):
        if task_name in self.tasks().keys():
            self.tasks()[task_name]['instance'].cancel()

    def cancel_all_tasks(self):
        for task in self.tasks():
            task.cancel()

    def remove_task(self, task_name):
        if task_name in self.tasks().keys():
            del self.tasks()[task_name]

    def remove_all_tasks(self):
        self.tasks().clear()

    def task_finished(self, task_name):
        pass

    # PIPELINES

    def run_pipeline(self, config):
        pass