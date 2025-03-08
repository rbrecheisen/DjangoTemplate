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
        return render(request, 'tasks/tasks.html', context={
            'task_names': task_manager.task_names(),
            'tasks': task_manager.tasks(),
            'auto_refresh': auto_refresh,
        })
    return HttpResponseForbidden(f'Wrong method ({request.method})')


@login_required
def task(request, task_name):
    if request.method == 'GET':
        data_manager = DataManager()
        return render(request, f'tasks/{task_name.lower()}', context={
            'task_name': task_name, 
            'task_description': TASK_REGISTRY[task_name]['description'],
            'filesets': data_manager.get_filesets(request.user)
        })
    return HttpResponseForbidden(f'Wrong method ({request.method})')


@login_required
def run_task(request, task_name):
    """
    1. Get input fileset IDs and parameters from request
    2. Pass them to task manager
    3. Run task
    4. Redirect to /tasks/
    """
    pass


@login_required
def cancel_task(request, task_name):
    pass


@login_required
def remove_task(request, task_name):
    pass


@login_required
def remove_all_tasks(request):
    pass