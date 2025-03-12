from .exampletask.exampletask import ExampleTask
from .copyfilestask.copyfilestask import CopyFilesTask
from .mergedirectoriestask.mergedirectoriestask import MergeDirectoriesTask


TASK_REGISTRY = {
    'ExampleTask': {
        'class': ExampleTask,
        'title': 'Example Task with two inputs and one output',
        'description': 'Some description',
        'inputs': [
            {
                'name': 'input1',
                'label': 'Select input 1',
            },
            {
                'name': 'input2',
                'label': 'Select input 2',
            },
        ],
        'outputs': [
            {
                'name': 'output1',
                'label': 'Enter name output 1 (optional)',
            }
        ],
        'params': [
            {
                'name': 'nr_iters', 
                'label': 'Number of iterations',
                'type': 'int', 
                'min': 0,
                'max': 100,
                'step': 1,
                'value': 5,
            },
            {
                'name': 'delay', 
                'label': 'Delay (s)',
                'type': 'int',
                'min': 0,
                'max': 10,
                'step': 1,
                'value': 1,
            },
        ],
    },
    'CopyFilesTask': {
        'class': CopyFilesTask,
        'title': 'Task that copies files from an input to an output directory',
        'description': '',
        'inputs': [
            {
                'name': 'input1',
                'label': 'Select input 1',
            },
        ],
        'outputs': [
            {
                'name': 'output1',
                'label': 'Enter name output 1 (optional)',
            }
        ],
        'params': [],
    },
    'MergeDirectoriesTask': {
        'class': MergeDirectoriesTask,
        'title': 'Task that copies files from two input directories to a single output directory',
        'description': '',
        'inputs': [
            {
                'name': 'input1',
                'label': 'Select input 1',
            },
            {
                'name': 'input2',
                'label': 'Select input 2',
            },
        ],
        'outputs': [
            {
                'name': 'output1',
                'label': 'Enter name output 1 (optional)',
            }
        ],
        'params': [
            {
                'name': 'keep_duplicates',
                'label': 'Keep duplicates in merge (appends number if needed)',
                'type': 'bool', 
                'value': False,
            }
        ],
    },
}