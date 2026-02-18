"""
Vercel Serverless Entry Point
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the Flask app
from app import app as application

# Vercel requires 'app' variable for @vercel/python
app = application
