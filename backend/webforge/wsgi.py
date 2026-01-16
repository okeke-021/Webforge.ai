"""
WSGI config for webforge project.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webforge.settings.production')

application = get_wsgi_application()
