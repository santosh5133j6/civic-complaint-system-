"""
Utility functions for file handling with Supabase Storage
"""
import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from config import Config
from database import get_supabase


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


def save_upload_file(file):
    """Save uploaded file to Supabase Storage and return public URL"""
    if file and allowed_file(file.filename):
        try:
            # Generate unique filename
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = f"{uuid.uuid4()}.{ext}"
            
            # Get Supabase client
            db = get_supabase()
            if not db:
                raise Exception("Supabase connection not available")
            
            # Read file content
            file_content = file.read()
            
            # Upload to Supabase Storage bucket 'complaint-images'
            try:
                result = db.storage.from_('complaint-images').upload(
                    filename,
                    file_content,
                    file_options={"content-type": f"image/{ext}"}
                )
                
                # Get public URL
                public_url = db.storage.from_('complaint-images').get_public_url(filename)
                
                print(f"File uploaded successfully to Supabase: {filename}")
                print(f"Public URL: {public_url}")
                
                return public_url
            except Exception as e:
                # If bucket doesn't exist or upload fails, save locally as fallback
                print(f"Supabase Storage error: {e}")
                print("Falling back to local storage...")
                return save_file_locally(file, filename, ext)
                
        except Exception as e:
            print(f"Error saving file: {e}")
            return None
    return None


def save_file_locally(file_obj, filename, ext):
    """Fallback: Save file to local filesystem"""
    try:
        # Reset file pointer if needed
        if hasattr(file_obj, 'seek'):
            file_obj.seek(0)
        else:
            # file_obj is bytes
            pass
            
        # Get absolute path to upload directory
        current_file = os.path.abspath(__file__)
        project_root = os.path.dirname(current_file)
        upload_dir = os.path.join(project_root, 'static', 'uploads')
        
        # Ensure upload directory exists
        os.makedirs(upload_dir, exist_ok=True)
        
        # Create full filepath
        filepath = os.path.join(upload_dir, filename)
        
        # Save file
        if isinstance(file_obj, bytes):
            with open(filepath, 'wb') as f:
                f.write(file_obj)
        else:
            file_obj.save(filepath)
        
        print(f"File saved locally: {filepath}")
        
        # Return relative URL
        return f"/static/uploads/{filename}"
    except Exception as e:
        print(f"Error saving file locally: {e}")
        return None


def format_datetime(dt_string):
    """Format datetime string for display"""
    try:
        dt = datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %I:%M %p')
    except:
        return dt_string


def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two coordinates in km"""
    from math import radians, sin, cos, sqrt, atan2
    
    R = 6371  # Earth's radius in km
    
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = R * c
    
    return distance


def get_status_color(status):
    """Get color for status badge"""
    colors = {
        'Pending': 'warning',
        'In Progress': 'info',
        'Resolved': 'success',
        'Rejected': 'danger'
    }
    return colors.get(status, 'secondary')


def get_priority_color(priority):
    """Get color for priority badge"""
    colors = {
        'Critical': 'danger',
        'High': 'warning',
        'Medium': 'info',
        'Low': 'secondary'
    }
    return colors.get(priority, 'secondary')
