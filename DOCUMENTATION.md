# 📚 Civic Issue Reporting System - Complete Documentation

**Version:** 1.0  
**Last Updated:** February 18, 2026  
**Repository:** https://github.com/santosh5133j6/civic-complaint-system-

---

## 📑 Table of Contents

1. [Project Overview](#1-project-overview)
2. [Features](#2-features)
3. [Technology Stack](#3-technology-stack)
4. [Quick Start (5 Minutes)](#4-quick-start-5-minutes)
5. [Installation Guide](#5-installation-guide)
6. [Database Setup (Supabase)](#6-database-setup-supabase)
7. [Configuration](#7-configuration)
8. [Running the Application](#8-running-the-application)
9. [Authentication System](#9-authentication-system)
10. [Testing Guide](#10-testing-guide)
11. [Deployment to Render](#11-deployment-to-render)
12. [File Structure](#12-file-structure)
13. [API Documentation](#13-api-documentation)
14. [Troubleshooting](#14-troubleshooting)
15. [Contributing](#15-contributing)

---

## 1. Project Overview

A **web-based, AI-assisted platform** for reporting and resolving civic issues using Flask, Machine Learning, and Supabase.

### Key Capabilities
- ✅ **Citizen Portal**: Submit complaints with photo evidence
- ✅ **AI Prioritization**: Machine learning ranks complaints by urgency
- ✅ **Admin Dashboard**: Track, manage, and resolve issues
- ✅ **Interactive Maps**: Visualize complaints geographically
- ✅ **Real-time Analytics**: Charts and statistics
- ✅ **Duplicate Detection**: Identifies similar complaints automatically

### Target Users
- **Citizens**: Report civic issues easily
- **Administrators**: Manage and resolve complaints efficiently
- **Government Agencies**: Track civic infrastructure problems

---

## 2. Features

### 🌟 Citizen Reporting Interface
- Submit complaints with image evidence
- Interactive map-based location selection
- Auto-detect current location using GPS
- Real-time form validation
- Auto-categorization using NLP

### 🤖 AI-Powered Prioritization
- Machine learning-based complaint prioritization
- Automatic categorization using NLP and keywords
- Duplicate detection using TF-IDF and cosine similarity
- Severity analysis from descriptions

### 📊 Admin Dashboard
- Real-time complaint visualization
- Interactive charts (Category, Priority, Status distribution)
- Department-wise routing
- Status tracking and updates
- Filter by status, priority, category, department
- Add admin notes to complaints

### 🗺️ Interactive Map View
- Visualize all complaints on OpenStreetMap
- Marker clustering for better performance
- Color-coded priority markers:
  - 🔴 Red: Critical/High
  - 🟡 Yellow: Medium
  - 🟢 Green: Low
- Detailed popup information for each complaint

### 🔐 Authentication & Security
- Secure admin login system
- Password hashing (SHA-256)
- Session-based authentication
- Protected routes with login_required decorator
- Public dashboard for citizens (no login required)

---

## 3. Technology Stack

### Backend
- **Framework**: Flask 3.0.0 (Python)
- **Database**: Supabase (PostgreSQL)
- **ML/AI**: scikit-learn, NLTK, sentence-transformers
- **Image Processing**: Pillow
- **Geolocation**: geopy
- **WSGI Server**: Gunicorn (production)

### Frontend
- **HTML5** with semantic markup
- **CSS3** with responsive Grid/Flexbox
- **JavaScript** (ES6+)
- **Charts**: Chart.js
- **Maps**: Leaflet.js with OpenStreetMap
- **Icons**: Unicode emojis

### Infrastructure
- **Storage**: Supabase Storage (images)
- **Deployment**: Render (recommended)
- **Version Control**: Git/GitHub

---

## 4. Quick Start (5 Minutes)

### Prerequisites
- Python 3.8 or higher
- Supabase account (free)
- Git installed
- Modern web browser

### Step 1: Install Dependencies
```powershell
# Clone or navigate to project folder
cd C:\Projects\civic-complaint-system

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install packages
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
```

### Step 2: Setup Database
1. Go to https://supabase.com and create free account
2. Create new project
3. Go to SQL Editor
4. Copy SQL from section 6 below
5. Run SQL to create tables

### Step 3: Configure Environment
```powershell
# Copy environment template
Copy-Item .env.example .env

# Edit .env with your Supabase credentials
# (See section 7 for details)
```

### Step 4: Run Application
```powershell
python app.py
```

Open browser: **http://localhost:5000**

---

## 5. Installation Guide

### For Windows

```powershell
# Navigate to project directory
cd "C:\Projects\civic-complaint-system"

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data for NLP features
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
```

### For Linux/Mac

```bash
# Navigate to project directory
cd ~/Projects/civic-complaint-system

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
```

### Verify Installation

```python
# Test imports
python -c "import flask, supabase, sklearn, nltk; print('All dependencies installed!')"
```

---

## 6. Database Setup (Supabase)

### Create Supabase Project

1. Visit https://supabase.com and sign up
2. Click "New Project"
3. Fill in:
   - **Name**: civic-complaint-system
   - **Database Password**: (save this!)
   - **Region**: Choose closest to you
4. Wait 2-3 minutes for initialization

### Run Database Schema

Go to **SQL Editor** in Supabase dashboard and run this SQL:

```sql
-- Create admins table
CREATE TABLE admins (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    department VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create complaints table
CREATE TABLE complaints (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    description TEXT NOT NULL,
    category VARCHAR(100) NOT NULL,
    priority VARCHAR(50) NOT NULL,
    priority_score INTEGER DEFAULT 0,
    status VARCHAR(50) DEFAULT 'Pending',
    department VARCHAR(255),
    latitude NUMERIC(10, 8),
    longitude NUMERIC(11, 8),
    address TEXT,
    image_url TEXT,
    is_duplicate BOOLEAN DEFAULT FALSE,
    similar_count INTEGER DEFAULT 0,
    admin_notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX idx_complaints_status ON complaints(status);
CREATE INDEX idx_complaints_priority ON complaints(priority);
CREATE INDEX idx_complaints_category ON complaints(category);
CREATE INDEX idx_complaints_created_at ON complaints(created_at DESC);
CREATE INDEX idx_complaints_location ON complaints(latitude, longitude);
CREATE INDEX idx_complaints_department ON complaints(department);
CREATE INDEX idx_complaints_duplicate ON complaints(is_duplicate);

-- Enable Row Level Security
ALTER TABLE complaints ENABLE ROW LEVEL SECURITY;
ALTER TABLE admins ENABLE ROW LEVEL SECURITY;

-- Create policies for public access
CREATE POLICY "Enable read access for all users" ON complaints
    FOR SELECT USING (true);

CREATE POLICY "Enable insert access for all users" ON complaints
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Enable update access for all users" ON complaints
    FOR UPDATE USING (true);

CREATE POLICY "Enable delete access for all users" ON complaints
    FOR DELETE USING (true);

-- Create trigger function for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger
CREATE TRIGGER update_complaints_updated_at 
    BEFORE UPDATE ON complaints
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Insert default admin account
INSERT INTO admins (username, email, password_hash, department)
VALUES ('admin', 'admin@civic.gov', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', 'All Departments');
```

### Setup Storage Bucket (for images)

1. Go to **Storage** in Supabase dashboard
2. Click **"New Bucket"**
3. Name: `complaint-images`
4. Public bucket: **Yes**
5. Click **"Create Bucket"**

### Configure Storage Policies

In SQL Editor, run:

```sql
-- Allow public access to images
CREATE POLICY "Public Read Access"
ON storage.objects FOR SELECT
USING (bucket_id = 'complaint-images');

CREATE POLICY "Public Insert Access"
ON storage.objects FOR INSERT
WITH CHECK (bucket_id = 'complaint-images');

CREATE POLICY "Public Update Access"
ON storage.objects FOR UPDATE
USING (bucket_id = 'complaint-images');
```

### Get Your Credentials

1. Go to **Settings** > **API**
2. Copy:
   - **Project URL** (like: https://xxx.supabase.co)
   - **anon/public** key (long string starting with "eyJ...")

---

## 7. Configuration

### Environment Variables

Create `.env` file in project root:

```env
# Supabase Configuration
SUPABASE_URL=https://wdncfyaeijhdamlxulko.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndkbmNmeWFlaWpoZGFtbHh1bGtvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njk0Mzc4NjksImV4cCI6MjA4NTAxMzg2OX0.bL4L9GIy5X1_GQC81oZOF8UzoTlqjlxFN0E5hC-ZDT0

# Flask Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production
FLASK_ENV=development
DEBUG=True

# Upload Configuration (optional)
MAX_FILE_SIZE=5242880
ALLOWED_EXTENSIONS=png,jpg,jpeg,gif
```

### Security Notes

⚠️ **IMPORTANT:**
- Never commit `.env` to Git (it's in `.gitignore`)
- Change `SECRET_KEY` in production
- Use strong random strings for production keys
- Change default admin password after first login

---

## 8. Running the Application

### Development Mode

```powershell
# Make sure virtual environment is activated
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Run Flask app
python app.py
```

The application will start on:
- **Local**: http://localhost:5000
- **Network**: http://192.168.x.x:5000

### Production Mode

```bash
# Using Gunicorn (recommended)
gunicorn app:app --bind 0.0.0.0:8000 --workers 4

# Or using Flask (not recommended for production)
FLASK_ENV=production python app.py
```

### Available Pages

| URL | Description | Auth Required |
|-----|-------------|---------------|
| `/` | Home - Submit complaint | No |
| `/public-dashboard` | View all complaints | No |
| `/map` | Map view of complaints | No |
| `/admin/login` | Admin login | No |
| `/admin` | Admin dashboard | Yes |
| `/admin/register` | Register new admin | Yes |

---

## 9. Authentication System

### Default Admin Credentials

**Username:** `admin`  
**Password:** `123`

> ⚠️ Change this immediately in production!

### Login Flow

1. Navigate to http://localhost:5000/admin
2. If not logged in→ redirected to `/admin/login`
3. Enter credentials
4. Click "Login"
5. Redirected to admin dashboard

### Two Dashboard Types

#### 1. Public Dashboard (No Login)
**URL:** `/public-dashboard`

**Features:**
- ✅ View all complaints (read-only)
- ✅ Filter by status, priority, category
- ✅ View statistics and charts
- ✅ Auto-refresh every 60 seconds
- ❌ Cannot modify complaints

#### 2. Admin Dashboard (Login Required)
**URL:** `/admin`

**Features:**
- ✅ All public features PLUS:
- ✅ Update complaint status
- ✅ Assign to departments
- ✅ Add admin notes
- ✅ Delete complaints
- ✅ Full CRUD operations

### Change Admin Password

Edit `auth.py`:

```python
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Update password
ADMIN_USERS = {
    'admin': hash_password('your_new_password'),
}
```

Or update directly in Supabase `admins` table.

---

## 10. Testing Guide

### Test Scenario 1: High Priority Complaint

**Input:**
```
Name: Rajesh Kumar
Email: rajesh@example.com
Phone: +91 9876543210
Category: Road Damage
Description: URGENT! Large pothole on Main Street causing accidents. 
             Multiple vehicles damaged. Immediate repair needed!
Location: Click on map
Image: Upload pothole photo
```

**Expected Result:**
- Priority: **Critical** or **High** (score 70+)
- Status: **Pending**
- Department: **Public Works Department**
- Success message with complaint ID

### Test Scenario 2: Auto-Categorization

**Input:**
```
Category: Auto-Detect from Description
Description: Garbage bins overflowing on Park Road. Waste not collected 
             for 5 days. Bad smell everywhere.
```

**Expected Result:**
- Auto-detected Category: **Waste Management**
- Priority: **High** (keywords detected)
- Department: **Sanitation Department**

### Test Scenario 3: Duplicate Detection

**Steps:**
1. Submit first complaint about pothole on Main Street
2. Submit second complaint with similar description and nearby location

**Expected Result:**
- Second complaint flagged as `is_duplicate: true`
- `similar_count: 1`
- Warning message showing similar complaint

### Test Scenario 4: Admin Operations

**Steps:**
1. Login to `/admin`
2. View complaint list
3. Click edit icon on a complaint
4. Change status to "In Progress"
5. Add note: "Assigned to field team"
6. Click Update

**Expected Result:**
- Status updated in database
- `updated_at` timestamp refreshed
- Admin note saved
- Success message displayed

### Test Scenario 5: Map View

**Steps:**
1. Submit 3-4 complaints at different locations
2. Navigate to `/map`
3. Zoom in/out
4. Click on markers

**Expected Result:**
- All complaints visible as markers
- Color-coded by priority
- Popup shows complaint details
- Markers cluster when zoomed out

---

## 11. Deployment to Render

### Why Render?
- ✅ **Full Flask support** (not serverless)
- ✅ **ML models work perfectly**
- ✅ **750 hours/month free**
- ✅ **Auto-deploy on git push**
- ✅ **Persistent storage**

### Deploy Steps

#### 1. Push to GitHub (if not already done)
```bash
cd C:\Projects\civic-complaint-system
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/civic-complaint-system.git
git push -u origin main
```

#### 2. Create Render Account
- Go to https://render.com
- Sign up with GitHub

#### 3. Create Web Service
- Click **"New +"** → **"Web Service"**
- Select your repository
- Click **"Connect"**

#### 4. Configure Service

**Settings:**
- **Name**: civic-complaint-system
- **Region**: Oregon (US West) or closest
- **Branch**: main
- **Runtime**: Python 3
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT`
- **Instance Type**: Free

#### 5. Add Environment Variables

Click "Environment Variables" and add:

| Key | Value |
|-----|-------|
| SUPABASE_URL | https://wdncfyaeijhdamlxulko.supabase.co |
| SUPABASE_KEY | eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... |
| SECRET_KEY | your-production-secret-key |

#### 6. Deploy
- Click **"Create Web Service"**
- Wait 3-5 minutes for deployment
- Your app will be live at: `https://civic-complaint-system.onrender.com`

### Post-Deployment

#### Update Supabase CORS
1. Supabase Dashboard → Settings → API
2. Add CORS origin: `https://your-app.onrender.com`

#### Update Storage CORS
1. Storage → Settings → CORS
2. Add:
```json
[
  {
    "origin": "https://your-app.onrender.com",
    "methods": ["GET", "POST", "PUT", "DELETE"],
    "headers": ["*"]
  }
]
```

### Auto-Deploy on Updates

```bash
# Make changes to code
git add .
git commit -m "Updated feature"
git push origin main

# Render auto-deploys! ✨
```

---

## 12. File Structure

```
civic-complaint-system/
│
├── 📄 app.py                  # Main Flask application (393 lines)
├── 📄 config.py               # Configuration settings
├── 📄 database.py             # Supabase operations
├── 📄 ml_models.py            # ML prioritization & NLP
├── 📄 utils.py                # Utility functions
├── 📄 auth.py                 # Authentication logic
│
├── 📋 requirements.txt        # Python dependencies
├── 📋 .env.example            # Environment template
├── 📋 .gitignore              # Git ignore rules
├── 📋 render.yaml             # Render config
│
├── 📚 DOCUMENTATION.md        # This file (complete guide)
│
├── 📁 templates/             # HTML templates
│   ├── index.html           # Citizen submission form
│   ├── admin.html           # Admin dashboard
│   ├── admin_login.html     # Login page
│   ├── admin_register.html  # Admin registration
│   ├── public_dashboard.html # Public view
│   ├── map.html             # Map view
│   └── about.html           # About page
│
├── 📁 static/               # Static assets
│   ├── css/
│   │   └── style.css       # Main stylesheet
│   ├── js/
│   │   ├── main.js         # Form logic
│   │   ├── admin.js        # Dashboard logic
│   │   ├── map.js          # Map logic
│   │   └── public_dashboard.js
│   ├── images/
│   │   └── background.jpg  # Custom background
│   └── uploads/            # Local image uploads
│
└── 📁 models/              # ML model storage
    └── .gitkeep

Total: 25+ files, ~3500 lines of code
```

---

## 13. API Documentation

### Base URL
**Local**: `http://localhost:5000`  
**Production**: `https://your-app.onrender.com`

### Endpoints

#### Submit Complaint
```http
POST /api/complaints
Content-Type: multipart/form-data

Parameters:
- name (string, required)
- email (string, required)
- phone (string, optional)
- description (string, required)
- category (string, required)
- latitude (float, required)
- longitude (float, required)
- address (string, optional)
- image (file, optional)

Response:
{
  "success": true,
  "complaint_id": 123,
  "priority": "High",
  "priority_score": 75,
  "is_duplicate": false,
  "similar_count": 0
}
```

#### Get All Complaints
```http
GET /api/complaints

Response:
{
  "complaints": [
    {
      "id": 1,
      "name": "John Doe",
      "description": "...",
      "category": "Road Damage",
      "priority": "High",
      "status": "Pending",
      "created_at": "2026-02-18T10:30:00Z",
      ...
    }
  ]
}
```

#### Get Single Complaint
```http
GET /api/complaints/{id}

Response:
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "description": "...",
  ...
}
```

#### Update Complaint (Admin only)
```http
PUT /api/complaints/{id}/update
Content-Type: application/json

Body:
{
  "status": "In Progress",
  "department": "Public Works",
  "admin_notes": "Assigned to team"
}

Response:
{
  "success": true,
  "message": "Complaint updated successfully"
}
```

#### Delete Complaint (Admin only)
```http
DELETE /api/complaints/{id}

Response:
{
  "success": true,
  "message": "Complaint deleted successfully"
}
```

---

## 14. Troubleshooting

### Problem: "Module not found" error
**Solution:**
```bash
pip install -r requirements.txt
# Ensure virtual environment is activated
```

### Problem: Supabase connection error
**Solution:**
- Verify `SUPABASE_URL` and `SUPABASE_KEY` in `.env`
- Check internet connection
- Ensure Supabase project is active

### Problem: NLTK data not found
**Solution:**
```python
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
```

### Problem: Image upload fails
**Solution:**
- Check `static/uploads/` directory exists
- Verify file size under 5MB
- Check file extension (png, jpg, jpeg, gif only)
- Ensure proper permissions on uploads folder

### Problem: Map not loading
**Solution:**
- Check internet connection (needs OpenStreetMap tiles)
- Verify Leaflet.js CDN is accessible
- Check browser console for JavaScript errors

### Problem: Admin login fails
**Solution:**
- Verify credentials: username=`admin`, password=`123`
- Check `admins` table in Supabase
- Clear browser cookies/session
- Check Flask secret key is set

### Problem: Port 5000 already in use
**Solution:**
```bash
# Find process using port 5000
netstat -ano | findstr :5000

# Kill process (Windows)
taskkill /PID <process_id> /F

# Or run on different port
flask run --port 5001
```

### Problem: Render deployment fails
**Solution:**
- Check build logs in Render dashboard
- Verify all environment variables are set
- Ensure `requirements.txt` is in root
- Check Python version compatibility

---

## 15. Contributing

### Development Setup

1. **Fork & Clone**
```bash
git clone https://github.com/YOUR_USERNAME/civic-complaint-system.git
cd civic-complaint-system
```

2. **Create Branch**
```bash
git checkout -b feature/your-feature-name
```

3. **Make Changes**
- Follow PEP 8 style guide for Python
- Add comments for complex logic
- Update documentation if needed

4. **Test Thoroughly**
- Test all affected features
- Check responsive design
- Verify database operations

5. **Commit & Push**
```bash
git add .
git commit -m "Add: your feature description"
git push origin feature/your-feature-name
```

6. **Create Pull Request**
- Go to GitHub repository
- Click "New Pull Request"
- Describe changes clearly

### Code Style

**Python:**
- Use 4 spaces for indentation
- Follow PEP 8 naming conventions
- Add docstrings to functions
- Keep functions under 50 lines

**JavaScript:**
- Use ES6+ features
- Use camelCase for variables
- Add JSDoc comments

**CSS:**
- Use BEM naming convention
- Keep selectors specific
- Use CSS variables for colors

---

## 📞 Support & Contact

### Documentation
- **Complete Guide**: This file (DOCUMENTATION.md)
- **GitHub**: https://github.com/santosh5133j6/civic-complaint-system-

### Tech Support
- **Supabase**: https://supabase.com/docs
- **Flask**: https://flask.palletsprojects.com
- **Render**: https://render.com/docs

### Report Issues
Open an issue on GitHub with:
- Description of problem
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)
- Error logs

---

## 📝 License

MIT License - Feel free to use for your projects!

---

## 🎉 Acknowledgments

- **Flask** team for excellent web framework
- **Supabase** for free PostgreSQL hosting
- **OpenStreetMap** for map tiles
- **Leaflet.js** for map library
- **Chart.js** for beautiful charts

---

**Last Updated:** February 18, 2026  
**Version:** 1.0.0  
**Status:** Production Ready ✅

---

**Quick Links:**
- 🏠 [Home Page](http://localhost:5000)
- 📊 [Public Dashboard](http://localhost:5000/public-dashboard)
- 🗺️ [Map View](http://localhost:5000/map)
- 🔐 [Admin Login](http://localhost:5000/admin/login)
- 🚀 [Deploy to Render](https://render.com)
- 📚 [Supabase Dashboard](https://supabase.com/dashboard)

**Happy Coding! 🎊**
