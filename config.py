import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Flask
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_ENV') == 'development'
    
    # Supabase
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    
    # Upload settings
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'static/uploads')
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 5242880))  # 5MB default
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # Map settings
    GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', '')
    
    # ML Model paths
    MODEL_PATH = 'models'
    
    # Complaint categories
    CATEGORIES = [
        'Road Damage',
        'Waste Management',
        'Streetlight',
        'Water Supply',
        'Sewage',
        'Parks & Gardens',
        'Public Transport',
        'Building Safety',
        'Noise Pollution',
        'Other'
    ]
    
    # Departments
    DEPARTMENTS = {
        'Road Damage': 'Public Works Department',
        'Waste Management': 'Sanitation Department',
        'Streetlight': 'Electricity Department',
        'Water Supply': 'Water Department',
        'Sewage': 'Water & Sewage Department',
        'Parks & Gardens': 'Parks Department',
        'Public Transport': 'Transport Department',
        'Building Safety': 'Building Department',
        'Noise Pollution': 'Environmental Department',
        'Other': 'General Administration'
    }
    
    # Priority levels
    PRIORITY_LEVELS = ['Critical', 'High', 'Medium', 'Low']
