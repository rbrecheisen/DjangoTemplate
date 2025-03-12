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
    """
    What should happen when a pipeline is executed? First of all, the pipeline needs input data.
    We cannot expect there to be an input fileset so files must be uploaded from disk. This means
    the pipeline needs an *input directory*. Next, we have a sequence of tasks that we wish to
    execute within this pipeline. Each task takes one or more filesets as input, has one or more
    outputs and zero or more parameters. Each task's output should serve as input for the next
    task. At the end of the pipeline, the last task's output becomes the output of the pipeline
    and should be saved to an *output directory*. The pipeline output fileset should be visible
    in the UI but all other task-related filesets must be deleted to save space.

    What to do with errors? Whenever a pipeline runs into problems, it should not clean up its
    intermediate filesets because we want to investigate what went wrong. 
    """
    if request.method == 'POST':
        return redirect('/tasks/')
    return HttpResponseForbidden(f'Wrong method ({request.method})')