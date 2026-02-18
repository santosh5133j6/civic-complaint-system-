"""
Database utilities for Supabase integration
"""
from supabase import create_client, Client
from config import Config
import os

# Initialize Supabase client
supabase: Client = None

def init_supabase():
    """Initialize Supabase client"""
    global supabase
    if Config.SUPABASE_URL and Config.SUPABASE_KEY and Config.SUPABASE_URL != 'your_supabase_project_url':
        try:
            supabase = create_client(
                supabase_url=Config.SUPABASE_URL,
                supabase_key=Config.SUPABASE_KEY
            )
            print("✅ Successfully connected to Supabase!")
            print(f"   Project URL: {Config.SUPABASE_URL}")
        except Exception as e:
            print(f"❌ ERROR: Failed to connect to Supabase: {e}")
            print("❌ Application requires Supabase connection")
            supabase = None
            raise Exception(f"Supabase connection failed: {e}")
    else:
        print("❌ ERROR: Supabase credentials not configured!")
        print("❌ Please configure .env file with SUPABASE_URL and SUPABASE_KEY")
        raise Exception("Supabase credentials not configured")
    return supabase

def get_supabase():
    """Get Supabase client instance"""
    global supabase
    if supabase is None:
        init_supabase()
    return supabase


class ComplaintDB:
    """Database operations for complaints"""
    
    @staticmethod
    def create_complaint(data):
        """Create a new complaint"""
        db = get_supabase()
        if not db:
            raise Exception("Supabase connection not available")
        
        result = db.table('complaints').insert(data).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def get_all_complaints(limit=100):
        """Get all complaints"""
        db = get_supabase()
        if not db:
            raise Exception("Supabase connection not available")
        
        result = db.table('complaints').select('*').order('created_at', desc=True).limit(limit).execute()
        return result.data
    
    @staticmethod
    def get_complaint_by_id(complaint_id):
        """Get complaint by ID"""
        db = get_supabase()
        if not db:
            raise Exception("Supabase connection not available")
        
        result = db.table('complaints').select('*').eq('id', complaint_id).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def update_complaint(complaint_id, data):
        """Update complaint"""
        db = get_supabase()
        if not db:
            raise Exception("Supabase connection not available")
        
        result = db.table('complaints').update(data).eq('id', complaint_id).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def delete_complaint(complaint_id):
        """Delete complaint and its image from storage, reset ID sequence if database is empty"""
        db = get_supabase()
        if not db:
            raise Exception("Supabase connection not available")
        
        # First, get the complaint to find the image URL
        complaint = db.table('complaints').select('image_url').eq('id', complaint_id).execute()
        
        # Delete the image from storage if it exists
        if complaint.data and len(complaint.data) > 0:
            image_url = complaint.data[0].get('image_url')
            if image_url and 'supabase.co/storage' in image_url:
                # Extract filename from URL (last part after /)
                filename = image_url.split('/')[-1]
                try:
                    db.storage.from_('complaint-images').remove([filename])
                except Exception as e:
                    print(f"Error deleting image from storage: {e}")
        
        # Delete the complaint from database
        result = db.table('complaints').delete().eq('id', complaint_id).execute()
        
        if result.data:
            # Check if there are any complaints left
            remaining = db.table('complaints').select('id').execute()
            
            # If no complaints left, reset the ID sequence to 1
            if not remaining.data or len(remaining.data) == 0:
                try:
                    db.rpc('execute_sql', {
                        'query': 'ALTER SEQUENCE complaints_id_seq RESTART WITH 1;'
                    }).execute()
                except:
                    # If RPC doesn't work, it's okay - sequence will continue normally
                    pass
            
            return True
        return False
    
    @staticmethod
    def get_complaints_by_status(status):
        """Get complaints by status"""
        db = get_supabase()
        if not db:
            raise Exception("Supabase connection not available")
        
        result = db.table('complaints').select('*').eq('status', status).execute()
        return result.data
    
    @staticmethod
    def get_complaints_by_category(category):
        """Get complaints by category"""
        db = get_supabase()
        if not db:
            raise Exception("Supabase connection not available")
        
        result = db.table('complaints').select('*').eq('category', category).execute()
        return result.data
    
    @staticmethod
    def get_statistics():
        """Get complaint statistics"""
        db = get_supabase()
        if not db:
            raise Exception("Supabase connection not available")
        
        all_complaints = db.table('complaints').select('*').execute().data
        
        stats = {
            'total': len(all_complaints),
            'pending': len([c for c in all_complaints if c.get('status') == 'Pending']),
            'in_progress': len([c for c in all_complaints if c.get('status') == 'In Progress']),
            'resolved': len([c for c in all_complaints if c.get('status') == 'Resolved']),
            'by_category': {},
            'by_priority': {}
        }
        
        for complaint in all_complaints:
            cat = complaint.get('category', 'Other')
            priority = complaint.get('priority', 'Medium')
            stats['by_category'][cat] = stats['by_category'].get(cat, 0) + 1
            stats['by_priority'][priority] = stats['by_priority'].get(priority, 0) + 1
        
        return stats


class UserDB:
    """Database operations for users"""
    
    @staticmethod
    def create_user(data):
        """Create a new user"""
        db = get_supabase()
        result = db.table('users').insert(data).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def get_user_by_email(email):
        """Get user by email"""
        db = get_supabase()
        result = db.table('users').select('*').eq('email', email).execute()
        return result.data[0] if result.data else None
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID"""
        db = get_supabase()
        result = db.table('users').select('*').eq('id', user_id).execute()
        return result.data[0] if result.data else None
