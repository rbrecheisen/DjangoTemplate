import os
import json

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
            inputs = {}
            for name in input_fileset_ids.keys():
                fileset_id = input_fileset_ids[name]
                fileset = data_manager.fileset(fileset_id)
                if fileset:
                    inputs[name] = [f.path() for f in fileset.files()]
            # Get output directories
            output_dirs = {}
            output_fileset_ids = []
            for name in output_fileset_names.keys():
                output_fileset_name = output_fileset_names[name]
                fileset = data_manager.create_fileset(user, output_fileset_name)
                output_dirs[name] = fileset.path()
                output_fileset_ids.append(fileset.id())
            # Instance task and run it
            task_instance = task_info['class'](
                inputs, output_dirs, params, self.task_finished)
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
        # Define inline function to resolve file and directory paths
        def resolve_dir(dir_path, config):
            if dir_path.startswith('__pipeline'):
                dir_name = dir_path.split('__')[1].split('.')[1]
                return config[dir_name]
            if dir_path.startswith('__'):
                items = dir_path.split('__')[1].split('.')
                task_name, key, name = items[0], items[1], items[2]
                for task_info in config['tasks']:
                    if task_info['name'] == task_name:
                        return task_info[key][name]
                raise RuntimeError()
            return dir_path
        # Parse config and print updated version
        for task_info in config['tasks']:
            for input_name in task_info['inputs'].keys():
                dir_path = resolve_dir(task_info['inputs'][input_name], config)
                task_info['inputs'][input_name] = dir_path
            for output_name in task_info['outputs'].keys():
                dir_path = resolve_dir(task_info['outputs'][output_name], config)
                task_info['outputs'][output_name] = dir_path
        print(json.dumps(config, indent=4))
        # Run tasks in sequence
        for task_info in config['tasks']:
            inputs = {}
            for input_name in task_info['inputs'].keys():
                input_files = []
                for f in os.listdir(task_info['inputs'][input_name]):
                    input_files.append(os.path.join(task_info['inputs'][input_name], f))
                inputs[input_name] = input_files
            outputs = {}
            for output_name in task_info['outputs'].keys():
                outputs[output_name] = task_info['outputs'][output_name]
            params = task_info['params']
            # Execute task
            task_instance = TASK_REGISTRY[task_info['name']]['class'](inputs, outputs, params, None)
            task_instance.start()
            task_instance.join()