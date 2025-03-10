from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest

from ..managers.logmanager import LogManager


def is_auto_refresh(request):
    return True if request.GET.get('auto-refresh', '0') == '1' else False


@login_required
def auth(_) -> HttpResponse:
    return HttpResponse(status=200)


@login_required
def custom_logout(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('/')


@login_required
def help(request):
    return render(request, 'help/index.html')


@login_required
def logs(request: HttpRequest) -> HttpResponse:
    manager = LogManager()
    if request.method == 'POST':
        manager.delete_messages()
    return render(request, 'logs.html', context={'messages': manager.get_messages()})