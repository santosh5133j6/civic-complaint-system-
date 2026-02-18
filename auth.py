"""
Simple authentication system for admin access using Supabase
"""
from functools import wraps
from flask import session, redirect, url_for, flash, request
import hashlib
from database import get_supabase
import requests
from config import Config

def hash_password(password):
    """Hash a password"""
    return hashlib.sha256(password.encode()).hexdigest()

def check_password(username, password):
    """Check if username and password are correct - using direct REST API"""
    try:
        # Use direct REST API call instead of Supabase client
        response = requests.get(
            f"{Config.SUPABASE_URL}/rest/v1/admins",
            headers={
                "apikey": Config.SUPABASE_KEY,
                "Authorization": f"Bearer {Config.SUPABASE_KEY}",
                "Content-Type": "application/json"
            },
            params={"username": f"eq.{username}"},
            timeout=10
        )
        
        if response.status_code == 200:
            admins = response.json()
            if admins and len(admins) > 0:
                admin = admins[0]
                return admin['password_hash'] == hash_password(password)
    except Exception as e:
        print(f"Error checking password: {e}")
    return False

def get_admin_department(username):
    """Get admin's department - using direct REST API"""
    try:
        response = requests.get(
            f"{Config.SUPABASE_URL}/rest/v1/admins",
            headers={
                "apikey": Config.SUPABASE_KEY,
                "Authorization": f"Bearer {Config.SUPABASE_KEY}",
                "Content-Type": "application/json"
            },
            params={"username": f"eq.{username}", "select": "department"},
            timeout=10
        )
        
        if response.status_code == 200:
            admins = response.json()
            if admins and len(admins) > 0:
                return admins[0]['department']
    except Exception as e:
        print(f"Error getting department: {e}")
    return None

def register_admin(username, password, email, department):
    """Register a new admin"""
    db = get_supabase()
    if not db:
        return False, "Supabase connection not available"
    
    try:
        # Check if username already exists
        result = db.table('admins').select('id').eq('username', username).execute()
        if result.data and len(result.data) > 0:
            return False, "Username already exists"
        
        # Create new admin
        admin_data = {
            'username': username,
            'email': email,
            'password_hash': hash_password(password),
            'department': department
        }
        
        db.table('admins').insert(admin_data).execute()
        return True, "Admin registered successfully"
    except Exception as e:
        print(f"Error registering admin: {e}")
        return False, str(e)

def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            flash('Please login to access the admin dashboard', 'warning')
            return redirect(url_for('admin_login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def is_admin_logged_in():
    """Check if admin is logged in"""
    return 'admin_logged_in' in session and session['admin_logged_in']
