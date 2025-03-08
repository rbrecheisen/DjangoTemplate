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
def view_png_file(request, fileset_id, file_id):
    if request.method == 'GET':
        f = FileModel.objects.get(pk=file_id)
        file_path = os.path.join(settings.MEDIA_ROOT, f.path())
        if os.path.exists(file_path):
            return render(request, 'views/pngview.html', context={'png_image': f, 'fileset_id': fileset_id})
    return Http404(f'File {file_id} not found')


@login_required
def view_csv_file(request, fileset_id, file_id):
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
            return render(request, 'views/csvview.html', context={'csv_file': f, 'headers': headers, 'rows': rows, 'fileset_id': fileset_id})
    return Http404(f'File {file_id} not found')


@login_required
def view_text_file(request, fileset_id, file_id):
    if request.method == 'GET':
        f = FileModel.objects.get(pk=file_id)
        file_path = os.path.join(settings.MEDIA_ROOT, f.path())
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f_obj:
                content = f_obj.read()
            return render(request, 'views/textview.html', context={'txt_file': f, 'content': content, 'fileset_id': fileset_id})
    return Http404(f'File {file_id} not found')
