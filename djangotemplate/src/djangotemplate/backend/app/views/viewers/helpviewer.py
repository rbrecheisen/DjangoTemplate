from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def help(request):
    return render(request, 'viewers/helpviewer/index.html')