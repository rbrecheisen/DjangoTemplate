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

    def run_task(self, task_name, inputs, params, wait_to_finish=False):
        task_info = TASK_REGISTRY.get(task_name, None)
        if task_info:
            if task_name in self.tasks().keys():
                raise RuntimeError(f'Task with name {task_name} already submitted. Clear task manager first')
            task_queue = queue.Queue()
            self.tasks()[task_name] = {
                'instance': task_info['class'](
                    inputs, params, task_queue, self.task_finished
                ),
                'queue': task_queue,
            }
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