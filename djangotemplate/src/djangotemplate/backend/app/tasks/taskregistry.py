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
            'param1',
            'param2',
        ],
        'outputs': [ # Always type fileset
            'output1',
        ],
    },
}