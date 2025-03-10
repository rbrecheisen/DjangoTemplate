import os
import sys

from django.core.management import execute_from_command_line


def run_server():
    appPath = os.path.join(os.path.abspath(__file__))
    appPath = os.path.dirname(appPath)
    appPath = os.path.join(appPath, 'backend')
    
    sys.path.append(appPath)
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    os.environ.setdefault('OAUTHLIB_INSECURE_TRANSPORT', '1')
    
    os.chdir(appPath)
    
    print('##############################################################################')
    print('#                      M Y   D J A N G O   A P P                             #')
    print('##############################################################################')
    
    execute_from_command_line(['manage.py', 'makemigrations'])
    execute_from_command_line(['manage.py', 'migrate'])
    execute_from_command_line(['manage.py', 'create_admin_user'])
    execute_from_command_line(['manage.py', 'clear_logs'])
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])


def main():
    print('Running My Django App server...')
    run_server()