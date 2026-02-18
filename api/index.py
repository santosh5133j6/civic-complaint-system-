"""
Vercel Serverless Entry Point
"""
import sys
import os

# Add parent directory to path to import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

# Create necessary directories
upload_path = os.path.abspath(app.config.get('UPLOAD_FOLDER', 'static/uploads'))
model_path = os.path.abspath(app.config.get('MODEL_PATH', 'models'))

os.makedirs(upload_path, exist_ok=True)
os.makedirs(model_path, exist_ok=True)

# Vercel expects a handler (or app for WSGI)
app = app
