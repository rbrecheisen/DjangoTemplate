import os
import shutil

from os.path import basename
from zipfile import ZipFile
from django.utils import timezone
from django.conf import settings
from django.db.models import Q

from ..models import FileModel, FileSetModel
from ..singleton import singleton


@singleton
class DataManager:
    @staticmethod
    def create_file(path, fileset):
        return FileModel.objects.create(
            _name=os.path.split(path)[1], _path=path, _fileset=fileset)
    
    @staticmethod
    def create_fileset(user, name=None):
        fileset_name = name
        if name is None or name == '':
            fileset_name = 'fileset-{}'.format(timezone.now().strftime('%Y%m%d%H%M%S'))
        fileset = FileSetModel.objects.create(_name=fileset_name, _owner=user)
        return fileset
       
    def create_fileset_from_uploaded_files(self, user, file_paths, file_names, fileset_name):
        if len(file_paths) == 0 or len(file_names) == 0:
            return None
        fileset = self.create_fileset(user, fileset_name)
        for i in range(len(file_paths)):
            source_path = file_paths[i]
            target_name = file_names[i]
            target_path = os.path.join(fileset.path(), target_name)
            if not settings.DOCKER: # Hack: to deal with "file in use" error Windows
                shutil.copy(source_path, target_path)
            else:
                shutil.move(source_path, target_path)
            self.create_file(target_path, fileset)
        return fileset

    @staticmethod
    def filesets(user):
        if not user.is_staff:
            return FileSetModel.objects.filter(Q(_owner=user))
        return FileSetModel.objects.all()

    @staticmethod
    def fileset(fileset_id):
        return FileSetModel.objects.get(pk=fileset_id)
    
    @staticmethod
    def fileset_by_name(fileset_name):
        return FileSetModel.objects.filter(_name=fileset_name).first()
    
    @staticmethod
    def files(fileset):
        return FileModel.objects.filter(_fileset=fileset).all()

    @staticmethod
    def delete_fileset(fileset):
        fileset.delete()

    @staticmethod
    def rename_fileset(fileset, new_name):
        fileset._name = new_name
        fileset.save()
        return fileset

    def create_zip_file_from_fileset(self, fileset):
        files = self.files(fileset)
        zip_file_path = os.path.join(fileset.path(), '{}.zip'.format(fileset.name()))
        with ZipFile(zip_file_path, 'w') as zip_obj:
            for f in files:
                zip_obj.write(f.path(), arcname=basename(f.path()))
        return zip_file_path