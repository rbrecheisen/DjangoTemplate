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

    def run_pipeline(self, config, user):
        # """
        # For each task I need an input_files_dict, output_dirs_dict and params.
        # Start with first task in the list. If it's the first, its inputs should be
        # set to the pipeline's inputs. 
        # """
        # data_manager = DataManager()
        # for task_info in config['tasks']:
        #     task_name = task_info['task_name']
        #     # Obtain input fileset IDs
        #     task_fileset_ids = {}
        #     for input in task_info['input_dirs']:
        #         f_names = []
        #         f_paths = []
        #         for f in os.listdir(input['path']):
        #             f_names.append(f)
        #             f_paths.append(os.path.join(input['path'], f))
        #             fileset = data_manager.create_fileset_from_uploaded_files(user, f_paths, f_names, input['name'])
        #             task_fileset_ids[input['name']] = fileset.id()
        #     task_output_fileset_names = {}
        #     for output in task_info['output_dirs']:
        #         output_fileset_name = os.path.split(output['path'])[1]
        #         task_output_fileset_names[output['name']] = output_fileset_name
        #     task_params = task_info['params']
        #     task_wait_to_finish = True
        #     self.run_task(task_name, task_fileset_ids, task_output_fileset_names, task_params, user, task_wait_to_finish)
        # # Get last task's output fileset and save in output_dir
        pass