import os

from os.path import basename
from zipfile import ZipFile
from django.utils import timezone
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
       
    @staticmethod
    def get_filesets(user):
        if not user.is_staff:
            return FileSetModel.objects.filter(Q(_owner=user))
        return FileSetModel.objects.all()

    @staticmethod
    def get_fileset(fileset_id):
        return FileSetModel.objects.get(pk=fileset_id)
    
    @staticmethod
    def get_fileset_by_name(fileset_name):
        return FileSetModel.objects.filter(_name=fileset_name).first()
    
    @staticmethod
    def get_fileset_by_name(fileset_name):
        return FileSetModel.objects.filter(_name=fileset_name).first()
    
    @staticmethod
    def get_files(fileset):
        return FileModel.objects.filter(_fileset=fileset).all()

    @staticmethod
    def delete_fileset(fileset):
        fileset.delete()

    @staticmethod
    def rename_fileset(fileset, new_name):
        fileset._name = new_name
        fileset.save()
        return fileset

    def get_zip_file_from_fileset(self, fileset):
        files = self.get_files(fileset)
        zip_file_path = os.path.join(fileset.path(), '{}.zip'.format(fileset.name()))
        with ZipFile(zip_file_path, 'w') as zip_obj:
            for f in files:
                zip_obj.write(f.path(), arcname=basename(f.path()))
        return zip_file_path