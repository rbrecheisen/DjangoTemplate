from django.urls import path

from .views.misc import auth, custom_logout, logs
from .views.filesets import filesets, fileset, upload_fileset, rename_fileset, delete_fileset, download_fileset
from .views.files import view_png_file, view_text_file, view_csv_file

from .views.viewers.helpviewer import help


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
    path('filesets/<str:fileset_id>/files/<str:file_id>/png', view_png_file),
    path('filesets/<str:fileset_id>/files/<str:file_id>/text', view_text_file),
    path('filesets/<str:fileset_id>/files/<str:file_id>/csv', view_csv_file),

    # Custom viewers
]