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
        active_tasks = task_manager.active_tasks()
        all_finished = True
        for task in active_tasks:
            if task.status() == 'running':
                all_finished = False
                break
        if all_finished:
            auto_refresh = False
        return render(request, 'tasks.html', context={
            'task_names': task_manager.task_names(),
            'active_tasks': active_tasks,
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
            'input_filesets': TASK_REGISTRY[task_name]['input_filesets'],
            'params': TASK_REGISTRY[task_name]['params'],
            'output_filesets': TASK_REGISTRY[task_name]['output_filesets'],
            'filesets': data_manager.filesets(request.user)
        })
    return HttpResponseForbidden(f'Wrong method ({request.method})')


@login_required
def run_task(request, task_name):
    if request.method == 'POST':
        data_manager = DataManager()
        task_info = TASK_REGISTRY[task_name]
        # Get input filesets from request parameters
        input_filesets = {}
        for input_fileset in task_info['input_filesets']:
            fileset_id = request.POST.get(input_fileset['name'])
            if fileset_id:
                input_filesets[input_fileset['name']] = data_manager.fileset(fileset_id)
        # Get task parameter values
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
        # Get output fileset names from request
        output_fileset_names = {}
        for output_fileset in task_info['output_filesets']:
            output_fileset_name = request.POST.get(output_fileset['name'], '')
            if output_fileset_name == '':
                output_fileset_name = create_name_with_timestamp(f'output-{task_name.lower()}')
            output_fileset_names[output_fileset['name']] = output_fileset_name
        # Run task though task manager
        task_manager = TaskManager()
        task_manager.run_task(task_name, input_filesets, output_fileset_names, params, request.user)
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