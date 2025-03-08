from django.urls import path

from .views.miscellaneous import auth, custom_logout, logs, help
from .views.filesets import filesets, fileset, upload_fileset, rename_fileset, delete_fileset, download_fileset
from .views.files import png, txt, csv


urlpatterns = [

    # Miscellaneous views
    path('auth', auth),
    path('help/', help),
    path('logs/', logs),
    path('accounts/logout/', custom_logout, name='logout'),

    # Filesets
    path('', filesets),
    path('filesets/', filesets),
    path('filesets/upload', upload_fileset),
    path('filesets/<str:fileset_id>', fileset),
    path('filesets/<str:fileset_id>/rename', rename_fileset),
    path('filesets/<str:fileset_id>/delete', delete_fileset),
    path('filesets/<str:fileset_id>/download', download_fileset),

    # Files
    path('filesets/<str:fileset_id>/files/<str:file_id>/png', png),
    path('filesets/<str:fileset_id>/files/<str:file_id>/text', txt),
    path('filesets/<str:fileset_id>/files/<str:file_id>/csv', csv),

    # Custom viewers
]