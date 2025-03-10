from .exampletask.exampletask import ExampleTask


TASK_REGISTRY = {
    'ExampleTask': {
        'class': ExampleTask,
        'title': 'Example Task with two inputs and one output',
        'description': 'Some description',
        'inputs': [ # Always type fileset
            {
                'name': 'input1',
                'label': 'Select input 1',
            },
            {
                'name': 'input2',
                'label': 'Select input 2',
            },
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
        'outputs': [ # Always type fileset
            {
                'name': 'output1',
                'label': 'Enter name for output 1',
            }
        ],
    },
}