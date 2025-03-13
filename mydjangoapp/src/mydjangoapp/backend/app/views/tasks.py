import json

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
            'pipeline_names': task_manager.pipeline_names(),
            'active_tasks': active_tasks,
            'auto_refresh': auto_refresh,
        })
    return HttpResponseForbidden(f'Wrong method ({request.method})')


@login_required
def task(request, task_name):
    if request.method == 'GET':
        data_manager = DataManager()
        return render(request, 'task.html', context={
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
        task_info = TASK_REGISTRY[task_name]
        # Get input filesets from request parameters
        input_fileset_ids = {}
        for input in task_info['inputs']:
            fileset_id = request.POST.get(input['name'])
            if fileset_id:
                input_fileset_ids[input['name']] = fileset_id
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
                if param_type == 'bool':
                    params[param['name']] = True if param_value == '1' else False
                if param_type == 'text':
                    params[param['name']] = param_value
        # Get output fileset names from request
        output_fileset_names = {}
        for output in task_info['outputs']:
            output_fileset_names[output['name']] = request.POST.get(output['name'], None)
        # Run task through task manager
        task_manager = TaskManager()
        task_manager.run_task(task_name, input_fileset_ids, output_fileset_names, params, request.user)
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


@login_required
def pipeline(request, pipeline_name):
    if request.method == 'GET':
        return render(request, 'pipeline.html', context={
            'pipeline_name': pipeline_name, 
            'pipeline_description': 'This is an example pipeline',
        })
    return HttpResponseForbidden(f'Wrong method ({request.method})')


@login_required
def run_pipeline(request, pipeline_name):
    if request.method == 'POST':
        pipeline_config = request.POST.get('pipeline_config', None)
        if pipeline_config:
            task_manager = TaskManager()
            task_manager.run_pipeline(json.loads(pipeline_config))
        return redirect('/tasks/')
    return HttpResponseForbidden(f'Wrong method ({request.method})')