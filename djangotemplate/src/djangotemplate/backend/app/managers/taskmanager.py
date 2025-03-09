import queue

from ..tasks.taskregistry import TASK_REGISTRY
from ..singleton import singleton


@singleton
class TaskManager:
    def __init__(self):
        self._tasks = {}

    # TASKS

    def tasks(self):
        sorted_tasks = sorted(self._tasks.values(), key=lambda task: task.created())
        return sorted_tasks
    
    def task_names(self):
        return sorted(TASK_REGISTRY.keys())
    
    def task_ok(self, task_info, inputs, outputs, params):
        for input_name in inputs.keys():
            if not input_name in task_info['inputs']:
                return False
        for output_name in inputs.keys():
            if not output_name in task_info['outputs']:
                return False
        for param_name in params.keys():
            if not param_name in task_info['params']:
                return False
        return True

    def run_task(self, task_name, inputs, outputs, params, wait_to_finish=False):
        task_info = TASK_REGISTRY.get(task_name, None)
        if task_info:
            # Check if the inputs and parameters match the task's info
            if not self.task_ok(task_info, inputs, outputs, params):
                raise RuntimeError(f'Task {task_name} inputs, outputs or parameters do not match registry')
            # If task is already in the list, cancel and remove it
            if task_name in self._tasks.keys():
                self.cancel_task(task_name)
                self.remove_task(task_name)
            # Add the new task to the list with its own queue
            task_queue = queue.Queue()
            self._tasks[task_name] = {
                'instance': task_info['class'](
                    inputs, outputs, params, task_queue, self.task_finished
                ),
                'queue': task_queue,
            }
            # Start the task and wait if necessary
            self._tasks[task_name]['instance'].start()
            if wait_to_finish:
                self._tasks[task_name]['instance'].join()

    def cancel_task(self, task_name):
        if task_name in self._tasks.keys():
            self._tasks[task_name]['instance'].cancel()

    def cancel_all_tasks(self):
        for task in self._tasks.values():
            task.cancel()

    def remove_task(self, task_name):
        if task_name in self._tasks.keys():
            del self._tasks[task_name]

    def remove_all_tasks(self):
        self._tasks.clear()

    def task_finished(self, task_name):
        task_info = TASK_REGISTRY.get(task_name, None)
        if task_info:
            # Get output fileset names
            pass

    # PIPELINES

    def run_pipeline(self, config):
        pass