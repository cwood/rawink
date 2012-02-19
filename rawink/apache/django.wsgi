import os
import sys
path = '/home/aebsr/rawink'
if path not in sys.path:
        sys.path.insert(0, '/home/aebsr/rawink')
        os.environ['DJANGO_SETTINGS_MODULE'] = 'myProject.settings'
        import django.core.handlers.wsgi
        application = django.core.handlers.wsgi.WSGIHandler()
