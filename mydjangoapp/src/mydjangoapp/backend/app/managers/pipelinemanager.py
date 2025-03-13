import os

from ..tasks.taskregistry import TASK_REGISTRY
from ..singleton import singleton
# from ..managers.datamanager import DataManager # This manager shouldn't do anything with SQL data
from ..managers.logmanager import LogManager

LOG = LogManager()


@singleton
class PipelineManager:
    def __init__(self):
        pass

    def run_pipeline(self, config={
        'name': 'ExamplePipeline',
        'input_dir': 'D:\\Mosamatic\\DjangoTemplate\\ExamplePipeline\\input',
        'output_dir': 'D:\\Mosamatic\\DjangoTemplate\\ExamplePipeline\\output',
        'tasks': [
            {
                'name': 'MergeDirectoriesTask',
                'inputs': {
                    'input1': '__pipeline.input_dir__',
                    'input2': '__pipeline.input_dir__'
                },
                'outputs': {
                    'output': 'D:\\Mosamatic\\DjangoTemplate\\ExamplePipeline\\MergeDirectoriesTask'
                },
                'params': {
                    'keep_duplicates': True
                }
            },
            {
                'name': 'CopyFilesTask',
                'inputs': {
                    'input': '__MergeDirectoriesTask.outputs.output__'
                },
                'outputs': {
                    'output': '__pipeline.output_dir__'
                },
                'params': None
            }
        ]
    }):
        # Parse config and report what you think needs to happen
        print('Running pipeline...')
        print(' - input_dir: {}'.format(config['input_dir']))
        print(' - output_dir: {}'.format(config['output_dir']))
        print('')
        print('Tasks:')
        for task_info in config['tasks']:
            print(' - {}'.format(task_info['name']))