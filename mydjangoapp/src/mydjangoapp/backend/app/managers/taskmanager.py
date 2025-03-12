import os

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
    
    def run_task(self, task_name, input_fileset_ids, output_fileset_names, params, user, wait_to_finish=False):
        task_info = TASK_REGISTRY.get(task_name, None)
        if task_info:
            data_manager = DataManager()
            # Get input files
            input_files_dict = {}
            for input_name in input_fileset_ids.keys():
                fileset_id = input_fileset_ids[input_name]
                fileset = data_manager.fileset(fileset_id)
                if fileset:
                    input_files_dict[input_name] = [f.path() for f in fileset.files()]
            # Get output directories
            output_dir_dict = {}
            output_fileset_ids = []
            for output_name in output_fileset_names.keys():
                output_fileset_name = output_fileset_names[output_name]
                fileset = data_manager.create_fileset(user, output_fileset_name)
                output_dir_dict[output_name] = fileset.path()
                output_fileset_ids.append(fileset.id())
            # Instance task and run it
            task_instance = task_info['class'](
                input_files_dict, output_dir_dict, params, self.task_finished)
            task_instance_id = task_instance.id()
            self._tasks[task_instance_id] = {
                'instance': task_instance,
                'output_fileset_ids': output_fileset_ids,
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
            # Create fileset for each output
            data_manager = DataManager()
            output_fileset_ids = self._tasks[task_id]['output_fileset_ids']
            for output_fileset_id in output_fileset_ids:
                fileset = data_manager.fileset(output_fileset_id)
                if fileset:
                    for f in os.listdir(fileset.path()):
                        data_manager.create_file(os.path.join(fileset.path(), f), fileset)

    # PIPELINES

    def pipeline_names(self):
        return ['ExamplePipeline']

    def run_pipeline(self, config):
        pass