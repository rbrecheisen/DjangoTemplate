from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from wsgiref.util import FileWrapper

from ..managers.fileuploadmanager import FileUploadManager
from ..managers.datamanager import DataManager


@login_required
def filesets(request):
    if request.method == 'GET':
        data_manager = DataManager()
        return render(request, 'filesets.html', context={'filesets': data_manager.get_filesets(request.user)})
    return HttpResponseForbidden(f'Wrong method ({request.method})')


@login_required
def fileset(request, fileset_id):
    if request.method == 'GET':
        data_manager = DataManager()
        fileset = data_manager.get_fileset(fileset_id)
        return render(request, 'fileset.html', context={'fileset': fileset, 'files': data_manager.get_files(fileset)})
    return HttpResponseForbidden(f'Wrong method ({request.method})')


@login_required
def upload_fileset(request):
    if request.method == 'POST':
        data_manager = DataManager()
        fileset_name = request.POST.get('fileset_name', None)
        file_paths, file_names = FileUploadManager().process_upload(request)
        data_manager.create_fileset_from_uploaded_files(request.user, file_paths, file_names, fileset_name)
        return redirect('/filesets/')
    return HttpResponseForbidden(f'Wrong method ({request.method})')


@login_required
def rename_fileset(request, fileset_id):
    if request.method == 'POST':
        data_manager = DataManager()
        fileset = data_manager.get_fileset(fileset_id)
        fileset = data_manager.rename_fileset(fileset, request.POST.get('new_name'))
        return redirect(f'/filesets/{fileset_id}')
    return HttpResponseForbidden(f'Wrong method ({request.method})')


@login_required
def delete_fileset(request, fileset_id):
    if request.method == 'GET':
        data_manager = DataManager()
        data_manager.delete_fileset(data_manager.get_fileset(fileset_id))
        return redirect('/filesets/')
    return HttpResponseForbidden(f'Wrong method ({request.method})')


@login_required
def download_fileset(request, fileset_id):
    if request.method == 'GET':
        data_manager = DataManager()
        zip_file_path = data_manager.get_zip_file_from_fileset(fileset)
        with open(zip_file_path, 'rb') as f:
            response = HttpResponse(FileWrapper(f), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="{}.zip"'.format(fileset.name)
        return response
    return HttpResponseForbidden(f'Wrong method ({request.method})')