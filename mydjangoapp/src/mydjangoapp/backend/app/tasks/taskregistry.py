from .exampletask.exampletask import ExampleTask


TASK_REGISTRY = {
    'ExampleTask': {
        'class': ExampleTask,
        'title': 'Example Task with two inputs and one output',
        'description': 'Some description',
        'input_filesets': [
            {
                'name': 'input1',
                'label': 'Select input 1',
            },
            {
                'name': 'input2',
                'label': 'Select input 2',
            },
        ],
        'output_filesets': [
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
}