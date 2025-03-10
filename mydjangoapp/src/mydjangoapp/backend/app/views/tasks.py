from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from ..managers.datamanager import DataManager
from ..managers.taskmanager import TaskManager
from ..tasks.taskregistry import TASK_REGISTRY
from ..utils import create_name_with_timestamp


@login_required
def tasks(request):
    if request.method == 'GET':
        auto_refresh = True if request.GET.get('auto-refresh', '0') == '1' else False
        task_manager = TaskManager()
        tasks = task_manager.tasks()
        all_finished = True
        for task in tasks:
            if task.status() == 'running':
                all_finished = False
                break
        if all_finished:
            auto_refresh = False
        return render(request, 'tasks.html', context={
            'task_names': task_manager.task_names(),
            'tasks': tasks,
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
                # Get parameter type
                param_type = param['type']
                if param_type == 'int':
                    params[param['name']] = int(param_value)
                if param_type == 'float':
                    params[param['name']] = float(param_value)
                if param_type == 'text':
                    params[param['name']] = param_value
        outputs = {}
        for output in task_info['outputs']:
            # output_name = request.POST.get(output['name'], '')
            # if output_name == '':
            #     output_name = create_name_with_timestamp(f'output-{task_name.lower()}')
            # outputs[output_name] = []
            outputs[output['name']] = []
        # Run task though task manager
        task_manager = TaskManager()
        task_manager.run_task(task_name, inputs, outputs, params, request.user)
        return redirect('/tasks/')
    return HttpResponseForbidden(f'Wrong method ({request.method})')


@login_required
def cancel_task(request, task_id):
    if request.method == 'GET':
        task_manager = TaskManager()
        task_manager.cancel_task(task_id)
        return redirect('/tasks/')
    return HttpResponseForbidden(f'Wrong method ({request.method})')


@login_required
def remove_task(request, task_id):
    if request.method == 'GET':
        task_manager = TaskManager()
        task_manager.remove_task(task_id)
        return redirect('/tasks/')
    return HttpResponseForbidden(f'Wrong method ({request.method})')