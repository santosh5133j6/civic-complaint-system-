"""
Flask Application - Crowdsourced Civic Issue Reporting System
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_cors import CORS
from datetime import datetime
import os
import json

from config import Config
from database import init_supabase, ComplaintDB, UserDB
from ml_models import ComplaintPrioritizer, DuplicateDetector
from utils import allowed_file, save_upload_file, format_datetime
from auth import login_required, check_password, is_admin_logged_in, register_admin, get_admin_department

app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = Config.SECRET_KEY  # Required for sessions
CORS(app)

# Initialize Supabase
init_supabase()

# Initialize ML models
prioritizer = ComplaintPrioritizer()
duplicate_detector = DuplicateDetector()

# Create necessary directories for production (Render, etc.)
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
os.makedirs(Config.MODEL_PATH, exist_ok=True)


@app.route('/')
def index():
    """Home page - Citizen complaint submission"""
    return render_template('index.html', categories=Config.CATEGORIES)


@app.route('/about')
def about():
    """About page - Information about the website"""
    return render_template('about.html')


@app.route('/submit-complaint', methods=['POST'])
def submit_complaint():
    """Handle complaint submission"""
    try:
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        description = request.form.get('description')
        category = request.form.get('category')
        latitude = float(request.form.get('latitude', 0))
        longitude = float(request.form.get('longitude', 0))
        address = request.form.get('address', '')
        
        # Handle file upload
        image_url = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename:
                image_url = save_upload_file(file)  # Returns full URL (Supabase) or relative path (local)
        
        # Auto-categorize if not provided
        if not category or category == 'auto':
            category = prioritizer.categorize_complaint(description)
        
        # Get existing complaints for similarity check
        existing_complaints = ComplaintDB.get_all_complaints()
        
        # Calculate priority
        priority, priority_score = prioritizer.calculate_priority_score(
            description, 
            category,
            image_count=1 if image_url else 0
        )
        
        # Add frequency boost
        location_data = {'latitude': latitude, 'longitude': longitude}
        frequency_boost = prioritizer.calculate_frequency_boost(
            category, 
            location_data, 
            existing_complaints
        )
        priority_score += frequency_boost
        
        # Re-evaluate priority with boost
        if priority_score >= 70:
            priority = 'Critical'
        elif priority_score >= 50:
            priority = 'High'
        elif priority_score >= 30:
            priority = 'Medium'
        else:
            priority = 'Low'
        
        # Check for duplicates
        is_duplicate, similar_complaints = duplicate_detector.check_duplicate(
            {'description': description},
            existing_complaints
        )
        
        # Determine department
        department = Config.DEPARTMENTS.get(category, 'General Administration')
        
        # Create complaint data
        complaint_data = {
            'name': name,
            'email': email,
            'phone': phone,
            'description': description,
            'category': category,
            'priority': priority,
            'priority_score': priority_score,
            'status': 'Pending',
            'department': department,
            'latitude': latitude,
            'longitude': longitude,
            'address': address,
            'image_url': image_url,
            'is_duplicate': is_duplicate,
            'similar_count': len(similar_complaints),
            'created_at': datetime.utcnow().isoformat(),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        # Save to database
        result = ComplaintDB.create_complaint(complaint_data)
        
        if result:
            return jsonify({
                'success': True,
                'message': 'Complaint submitted successfully!',
                'complaint_id': result.get('id'),
                'priority': priority,
                'is_duplicate': is_duplicate,
                'similar_complaints': similar_complaints[:3]  # Top 3 similar
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to submit complaint. Please try again.'
            }), 500
    
    except Exception as e:
        print(f"Error submitting complaint: {e}")
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500


@app.route('/admin')
@login_required
def admin_dashboard():
    """Admin dashboard - requires login"""
    try:
        complaints = ComplaintDB.get_all_complaints()
        stats = ComplaintDB.get_statistics()
        
        return render_template(
            'admin.html',
            complaints=complaints,
            stats=stats,
            categories=Config.CATEGORIES,
            departments=Config.DEPARTMENTS,
            admin_user=session.get('admin_username')
        )
    except Exception as e:
        print(f"Error loading admin dashboard: {e}")
        return render_template('admin.html', complaints=[], stats={}, admin_user=session.get('admin_username'))


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if check_password(username, password):
            session['admin_logged_in'] = True
            session['admin_username'] = username
            department = get_admin_department(username)
            session['admin_department'] = department if department else 'Unknown'
            flash('Login successful!', 'success')
            
            # Redirect to next page or admin dashboard
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('admin_login.html')


@app.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    """Admin registration page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        email = request.form.get('email')
        department = request.form.get('department')
        
        # Validation
        if not all([username, password, confirm_password, email, department]):
            flash('All fields are required', 'error')
        elif password != confirm_password:
            flash('Passwords do not match', 'error')
        elif len(password) < 6:
            flash('Password must be at least 6 characters', 'error')
        else:
            success, message = register_admin(username, password, email, department)
            if success:
                flash(message + ' Please login.', 'success')
                return redirect(url_for('admin_login'))
            else:
                flash(message, 'error')
    
    # Get unique department names
    department_list = sorted(set(Config.DEPARTMENTS.values()))
    return render_template('admin_register.html', departments=department_list)


@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))


@app.route('/public-dashboard')
def public_dashboard():
    """Public complaints dashboard - accessible to everyone"""
    try:
        complaints = ComplaintDB.get_all_complaints()
        stats = ComplaintDB.get_statistics()
        
        return render_template(
            'public_dashboard.html',
            complaints=complaints,
            stats=stats,
            categories=Config.CATEGORIES
        )
    except Exception as e:
        print(f"Error loading public dashboard: {e}")
        return render_template('public_dashboard.html', complaints=[], stats={})


@app.route('/api/complaints')
def get_complaints():
    """API endpoint to get all complaints"""
    try:
        complaints = ComplaintDB.get_all_complaints()
        return jsonify({
            'success': True,
            'complaints': complaints
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/complaints/<int:complaint_id>')
def get_complaint(complaint_id):
    """API endpoint to get single complaint"""
    try:
        complaint = ComplaintDB.get_complaint_by_id(complaint_id)
        if complaint:
            return jsonify({
                'success': True,
                'complaint': complaint
            })
        return jsonify({
            'success': False,
            'message': 'Complaint not found'
        }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/complaints/<int:complaint_id>/update', methods=['POST'])
@login_required
def update_complaint(complaint_id):
    """Update complaint status - admin only"""
    try:
        data = request.get_json()
        update_data = {
            'status': data.get('status'),
            'updated_at': datetime.utcnow().isoformat()
        }
        
        if 'notes' in data:
            update_data['admin_notes'] = data['notes']
        
        result = ComplaintDB.update_complaint(complaint_id, update_data)
        
        if result:
            return jsonify({
                'success': True,
                'message': 'Complaint updated successfully',
                'complaint': result
            })
        return jsonify({
            'success': False,
            'message': 'Failed to update complaint'
        }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/complaints/<int:complaint_id>/delete', methods=['DELETE', 'POST'])
@login_required
def delete_complaint(complaint_id):
    """Delete complaint - admin only"""
    try:
        result = ComplaintDB.delete_complaint(complaint_id)
        
        if result:
            return jsonify({
                'success': True,
                'message': 'Complaint deleted successfully'
            })
        return jsonify({
            'success': False,
            'message': 'Failed to delete complaint'
        }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/statistics')
def get_statistics():
    """Get complaint statistics"""
    try:
        stats = ComplaintDB.get_statistics()
        return jsonify({
            'success': True,
            'statistics': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/map')
def map_view():
    """Map view of all complaints"""
    try:
        complaints = ComplaintDB.get_all_complaints()
        return render_template('map.html', complaints=complaints)
    except Exception as e:
        print(f"Error loading map: {e}")
        return render_template('map.html', complaints=[])


# Template filters
@app.template_filter('datetime')
def datetime_filter(value):
    """Format datetime for templates"""
    return format_datetime(value)


if __name__ == '__main__':
    # Create necessary directories with absolute paths
    upload_path = os.path.abspath(Config.UPLOAD_FOLDER)
    model_path = os.path.abspath(Config.MODEL_PATH)
    
    os.makedirs(upload_path, exist_ok=True)
    os.makedirs(model_path, exist_ok=True)
    
    print(f"✓ Upload directory created: {upload_path}")
    print(f"✓ Model directory created: {model_path}")
    
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=5000)
