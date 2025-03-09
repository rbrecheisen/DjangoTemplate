from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from ..managers.datamanager import DataManager
from ..managers.taskmanager import TaskManager
from ..tasks.taskregistry import TASK_REGISTRY


@login_required
def tasks(request):
    if request.method == 'GET':
        auto_refresh = True if request.GET.get('auto-refresh', '0') == '1' else False
        task_manager = TaskManager()
        all_finished = True
        for task in task_manager.tasks():
            if task.status() == 'running':
                all_finished = False
                break
        if all_finished:
            auto_refresh = False
        return render(request, 'tasks.html', context={
            'task_names': task_manager.task_names(),
            'tasks': task_manager.tasks(),
            'auto_refresh': auto_refresh,
        })
    return HttpResponseForbidden(f'Wrong method ({request.method})')


@login_required
def task(request, task_name):
    if request.method == 'GET':
        data_manager = DataManager()
        return render(request, f'task.html', context={
            'task_name': task_name, 
            'task_description': TASK_REGISTRY[task_name]['description'],
            'inputs': TASK_REGISTRY[task_name]['inputs'],
            'params': TASK_REGISTRY[task_name]['params'],
            'outputs': TASK_REGISTRY[task_name]['outputs'],
            'filesets': data_manager.filesets(request.user)
        })
    return HttpResponseForbidden(f'Wrong method ({request.method})')


@login_required
def run_task(request, task_name):
    """
    1. Get input fileset IDs and parameters from request (ensure correct data types)
    2. Pass them to task manager
    3. Run task
    4. Redirect to /tasks/
    """
    if request.method == 'POST':
        # Get inputs and parameters from request
        data_manager = DataManager()
        task_info = TASK_REGISTRY[task_name]
        inputs = {}
        for input in task_info['inputs']:
            fileset_id = request.POST.get(input['name'])
            if fileset_id:
                inputs[input['name']] = data_manager.fileset(fileset_id)
        params = {}
        for param in task_info['params']:
            param_value = request.POST.get(param['name'], None)
            if param_value:
                params[param['name']] = param_value
        outputs = {}
        for output in task_info['outputs']:
            outputs[output['name']] = []
        # Run task though task manager
        task_manager = TaskManager()
        task_manager.run_task(task_name, inputs, outputs, params)
        return redirect('/tasks/')
    return HttpResponseForbidden(f'Wrong method ({request.method})')


@login_required
def cancel_task(request, task_name):
    pass


@login_required
def remove_task(request, task_name):
    pass


@login_required
def remove_all_tasks(request):
    pass