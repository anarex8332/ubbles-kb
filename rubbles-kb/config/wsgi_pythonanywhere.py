import os
import sys

# Путь к проекту на PythonAnywhere
path = '/home/anarex8332/ubbles-kb'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()