import queue

from ..tasks.taskregistry import TASK_REGISTRY
from ..singleton import singleton
from ..managers.datamanager import DataManager
from ..managers.logmanager import LogManager

LOG = LogManager()


@singleton
class TaskManager:
    def __init__(self):
        self._tasks = {}

    def active_tasks(self):
        tasks = []
        for task_name in self._tasks.keys():
            tasks.append(self._tasks[task_name]['instance'])
        sorted_tasks = sorted(tasks, key=lambda task: task.created())
        return sorted_tasks
    
    def task_names(self):
        return sorted(TASK_REGISTRY.keys())
    
    def run_task(self, task_name, input_filesets, output_fileset_names, params, user, wait_to_finish=False):
        task_info = TASK_REGISTRY.get(task_name, None)
        if task_info:
            # Get user from one of the input filesets. Does that make sense?
            # Add the new task to the list with its own queue
            task_queue = queue.Queue()
            task_instance = task_info['class'](
                input_filesets, output_fileset_names, params, task_queue, self.task_finished)
            task_instance_id = task_instance.id()
            self._tasks[task_instance_id] = {
                'instance': task_instance,
                'queue': task_queue,
                'user': user,
            }
            # Start the task and wait if necessary
            self._tasks[task_instance_id]['instance'].start()
            if wait_to_finish:
                self._tasks[task_instance_id]['instance'].join()

    def cancel_task(self, task_name):
        if task_name in self._tasks.keys():
            self._tasks[task_name]['instance'].cancel()

    def cancel_all_tasks(self):
        for task in self._tasks.values():
            task.cancel()

    def remove_task(self, task_id):
        if task_id in self._tasks.keys():
            del self._tasks[task_id]

    def remove_all_tasks(self):
        self._tasks.clear()

    def task_finished(self, task_id):
        task_instance = self._tasks[task_id]['instance']
        task_info = TASK_REGISTRY.get(task_instance.name(), None)
        if task_info:
            # Get outputs
            task_queue = self._tasks[task_id]['queue']
            outputs = task_queue.get() # Dictionary of lists of file paths
            # Get user associated with task
            user = self._tasks[task_id]['user']
            # Create fileset for each output
            data_manager = DataManager()
            for output_name in outputs.keys():
                fileset = data_manager.create_fileset(user, output_name)
                file_paths = outputs[output_name]                
                for file_path in file_paths:
                    data_manager.create_file(file_path, fileset)

    # PIPELINES

    def pipeline_names(self):
        return ['ExamplePipeline']

    def run_pipeline(self, config):
        pass