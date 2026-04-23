# PythonAnywhere WSGI Configuration File
# Copy this content to: /var/www/mothishraghavendra_pythonanywhere_com_wsgi.py
# (after creating web app on PythonAnywhere)

import sys
import os
from pathlib import Path

# ============================================================================
# Add your project directory to the sys.path
# ============================================================================
path = '/home/mothishraghavendra/educycle'  # Change username to yours
if path not in sys.path:
    sys.path.insert(0, path)

# ============================================================================
# Set up Django settings module
# ============================================================================
os.environ['DJANGO_SETTINGS_MODULE'] = 'Educycle.settings'

# ============================================================================
# Activate your virtual environment
# ============================================================================
virtualenv = '/home/mothishraghavendra/.virtualenvs/educycle_env/lib/python3.10/site-packages'
if virtualenv not in sys.path:
    sys.path.insert(0, virtualenv)

# ============================================================================
# Import Django WSGI application
# ============================================================================
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
