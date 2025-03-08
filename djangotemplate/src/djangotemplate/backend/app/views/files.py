import os
import csv

from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404

from ..managers.logmanager import LogManager
from ..models import FileModel

LOG = LogManager()


@login_required
def png(request, fileset_id, file_id):
    if request.method == 'GET':
        f = FileModel.objects.get(pk=file_id)
        file_path = os.path.join(settings.MEDIA_ROOT, f.path())
        if os.path.exists(file_path):
            return render(request, 'file.html', context={'file': f, 'file_type': 'png', 'fileset_id': fileset_id})
    return Http404(f'File {file_id} not found')


@login_required
def csv(request, fileset_id, file_id):
    if request.method == 'GET':
        f = FileModel.objects.get(pk=file_id)
        file_path = os.path.join(settings.MEDIA_ROOT, f.path())
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f_obj:
                csv_reader = csv.reader(f_obj, delimiter=';')
                data = list(csv_reader)
            if not data:
                raise Http404(f'File {file_id} is empty')
            headers = data[0]  # First row as headers
            rows = data[1:]
            return render(request, 'file.html', context={'file': f, 'file_type': 'csv', 'fileset_id': fileset_id, 'headers': headers, 'rows': rows})
    return Http404(f'File {file_id} not found')


@login_required
def txt(request, fileset_id, file_id):
    if request.method == 'GET':
        f = FileModel.objects.get(pk=file_id)
        file_path = os.path.join(settings.MEDIA_ROOT, f.path())
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f_obj:
                content = f_obj.read()
            return render(request, 'file.html', context={'file': f, 'file_type': 'txt', 'fileset_id': fileset_id, 'content': content})
    return Http404(f'File {file_id} not found')
