# backend/pypath.py
import os
import sys

# Add the backend directory to Python path
backend_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_path not in sys.path:
    sys.path.append(backend_path)

# Add the app directory to Python path
app_path = os.path.join(backend_path, 'app')
if app_path not in sys.path:
    sys.path.append(app_path)
    