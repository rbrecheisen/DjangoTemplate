import os
import math
import uuid
import shutil

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.dispatch import receiver


class FileSetModel(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    _name = models.CharField(max_length=1024, editable=True, null=False)
    _path = models.CharField(max_length=2048, editable=False, null=True, unique=True)
    _created = models.DateTimeField(auto_now_add=True)
    _owner = models.ForeignKey(
        User, editable=False, related_name='+', on_delete=models.CASCADE)
    
    def id(self):
        return self._id
    
    def name(self):
        return self._name
    
    def path(self):
        return self._path
    
    def created(self):
        return self._created
    
    def owner(self):
        return self._owner

    def size(self):
        return FileModel.objects.filter(_fileset=self).count()
    
    def files(self):
        return FileModel.objects.filter(_fileset=self).all()
    
    def __str__(self):
        return self.name()


class FileModel(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    _name = models.CharField(max_length=256, editable=False, null=False)
    _path = models.CharField(max_length=2048, editable=False, null=False, unique=False) # unique=False because multiple filesets may refer to same file
    _fileset = models.ForeignKey(FileSetModel, on_delete=models.CASCADE)

    def id(self):
        return self._id
    
    def name(self):
        return self._name
    
    def path(self):
        return self._path
    
    def fileset(self):
        return self._fileset
    
    def size(self):
        return int(math.floor(
            os.path.getsize(os.path.join(
                settings.MEDIA_ROOT, self.path())) / 1000.0))

    def __str__(self):
        return os.path.split(str(self.path()))[1]


class LogOutputModel(models.Model):
    _id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    _mode = models.CharField(max_length=8, editable=False, null=False, choices=[
        ('info', 'info'),
        ('warning', 'warning'),
        ('error', 'error'),
    ], default='info')
    _timestamp = models.DateTimeField(auto_now_add=True)
    _message = models.CharField(max_length=1024, editable=False, null=False)

    def id(self):
        return self._id
    
    def mode(self):
        return self._mode
    
    def timestamp(self):
        return self._timestamp
    
    def message(self):
        return self._message

    def __str__(self):
        return f'[{self.timestamp()}] - [{self.mode()}]: {self.message()}'


@receiver(models.signals.post_save, sender=FileSetModel)
def fileset_post_save(sender, instance, **kwargs):
    if not instance.path():
        instance._path = os.path.join(settings.MEDIA_ROOT, str(instance.id()))
        os.makedirs(instance.path(), exist_ok=False)
        instance.save()


@receiver(models.signals.post_delete, sender=FileSetModel)
def fileset_post_delete(sender, instance, **kwargs):
    if os.path.isdir(instance.path()):
        shutil.rmtree(instance.path())
