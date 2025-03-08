TASK_REGISTRY = {
    'ExampleTask': {
        'class': None,
        'title': 'Example Task with two inputs and one output',
        'description': 'Some description',
        'inputs': [ # Always type fileset
            'input1',
            'input2',
        ],
        'params': [
            {
                'name': 'param1', 
                'label': 'Parameter 1',
                'type': 'int', 
                'min': 0,
                'max': 100,
                'step': 1,
                'value': 50,
            },
            {
                'name': 'param2', 
                'label': 'Parameter 2',
                'type': 'text',
                'value': '',
            },
        ],
        'outputs': [ # Always type fileset
            'output1',
        ],
    },
}