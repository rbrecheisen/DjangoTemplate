import os
import time
import pytest

from django.contrib.auth.models import User

from app.managers.taskmanager import TaskManager
from app.managers.datamanager import DataManager

DATA_DIR = 'D:\\Mosamatic\\Mosamatic Desktop 2.0\\input'


@pytest.mark.django_db
def test_user_can_run_example_task():

    # Create test user
    user = User.objects.create_user('test_user')

    # Retrieve files for inputs
    file_names = []
    file_paths = []
    for f in os.listdir(DATA_DIR):
        file_names.append(f)
        file_paths.append(os.path.join(DATA_DIR, f))

    data_manager = DataManager()
    task_manager = TaskManager()

    nr_iters, delay = 5, 2

    # Run example task and check its output has length > 0
    task_manager.run_task(task_name='ExampleTask', input_filesets={
        'input1': data_manager.create_fileset_from_uploaded_files(user, file_paths, file_names, 'input1'),
        'input2': data_manager.create_fileset_from_uploaded_files(user, file_paths, file_names, 'input2'),
    }, output_fileset_ids={
        'output1': [],
    }, params={
        'nr_iters': nr_iters,
        'delay': delay,
    }, user=user, wait_to_finish=True)

    # Wait a few seconds for the output to appear
    duration = nr_iters * delay + 1
    print(f'Waiting {duration} seconds...')
    time.sleep(duration)

    # Get output fileset
    output_fileset = data_manager.fileset_by_name('output1')
    assert output_fileset