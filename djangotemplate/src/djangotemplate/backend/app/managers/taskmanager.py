import queue

from ..tasks.taskregistry import TASK_REGISTRY
from ..singleton import singleton
from ..managers.datamanager import DataManager
from ..managers.logmanager import LogManager

LOG = LogManager()


@singleton
class TaskManager:
    def __init__(self, user=None):
        self._user = user
        self._tasks = {}

    def user(self):
        return self._user

    # TASKS

    def tasks(self):
        tasks = []
        for task_name in self._tasks.keys():
            tasks.append(self._tasks[task_name]['instance'])
        sorted_tasks = sorted(tasks, key=lambda task: task.created())
        return sorted_tasks
    
    def task_names(self):
        return sorted(TASK_REGISTRY.keys())
    
    def task_ok(self, task_info, inputs, outputs, params):
        for input in task_info['inputs']:
            if input['name'] not in inputs.keys():
                LOG.error('Input {} missing'.format(input['name']))
                return False
        for output in task_info['outputs']:
            if output['name'] not in outputs.keys():
                LOG.error('Output {} missing'.format(output['name']))
                return False
        for param in task_info['params']:
            if param['name'] not in params.keys():
                LOG.error('Parameter {} missing'.format(param['name']))
                return False
            # TODO: Check param types as well
        return True
    
    def run_task(self, task_name, inputs, outputs, params, wait_to_finish=False):
        task_info = TASK_REGISTRY.get(task_name, None)
        if task_info:
            # Check if task inputs, outputs and params match registry
            if not self.task_ok(task_info, inputs, outputs, params):
                raise RuntimeError(f'Inputs, outputs or parameters provided for {task_name} do not match registry')
            # If task is already in the list, cancel and remove it
            if task_name in self._tasks.keys():
                self.cancel_task(task_name)
                self.remove_task(task_name)
            # Get user from one of the input filesets. Does that make sense?
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
            # Get outputs
            task_queue = self._tasks[task_name]['queue']
            outputs = task_queue.get() # Dictionary of lists of file paths
            # Create fileset for each output
            data_manager = DataManager()
            for output in task_info['outputs']:
                fileset = data_manager.create_fileset(self.user(), output['name'])
                file_paths = outputs[output['name']]
                for file_path in file_paths:
                    data_manager.create_file(file_path, fileset)

    # PIPELINES

    def run_pipeline(self, config):
        pass