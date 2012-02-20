import os, os.path
import sys

# Unless your project is already on your PYTHONPATH by default, you need to add it:
# project_directory should point to your project's parent directory.
cwd = os.path.dirname(__file__)
project_directory = os.path.join(cwd, '..')
if project_directory not in sys.path:
    sys.path.append(project_directory);

os.environ['DJANGO_SETTINGS_MODULE'] = 'rawink.settings'

# Create the wsgi application.
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

# Run the monitor
from django.conf import settings
if settings.DEBUG:
    try:
        from rawink import monitor
    except ImportError:
        pass
    else:
        monitor.start(interval=1.0)
