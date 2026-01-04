"""
WSGI config for souq_khidma project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'souq_khidma.settings')

application = get_wsgi_application()

