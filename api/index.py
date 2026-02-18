import sys
import os

# Add parent directory to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import Flask app
from app import app

# This is the WSGI application Vercel will use
def handler(environ, start_response):
    return app(environ, start_response)
