# Project Structure

```
civic-issue-reporting/
│
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── database.py                 # Supabase database operations
├── ml_models.py                # ML prioritization and NLP
├── utils.py                    # Utility functions
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
│
├── templates/                  # HTML templates
│   ├── index.html             # Citizen complaint form
│   ├── admin.html             # Admin dashboard
│   └── map.html               # Map view
│
├── static/                     # Static files
│   ├── css/
│   │   └── style.css          # Main stylesheet
│   ├── js/
│   │   ├── main.js            # Complaint form logic
│   │   ├── admin.js           # Admin dashboard logic
│   │   └── map.js             # Map view logic
│   └── uploads/               # Uploaded images
│
├── models/                     # ML model storage
│
├── README.md                   # Main documentation
├── QUICKSTART.md              # Quick start guide
├── SUPABASE_SETUP.md          # Database setup guide
├── run.bat                    # Windows launcher
└── run.sh                     # Linux/Mac launcher
```

## File Descriptions

### Core Application Files

#### app.py
Main Flask application with routes:
- `/` - Home page (complaint submission)
- `/submit-complaint` - Handle form submission
- `/admin` - Admin dashboard
- `/map` - Map view
- `/api/complaints` - REST API for complaints
- `/api/statistics` - Statistics API

#### config.py
Configuration class containing:
- Flask settings
- Supabase credentials
- Upload settings
- Categories and departments
- Priority levels

#### database.py
Supabase integration:
- `init_supabase()` - Initialize connection
- `ComplaintDB` - Complaint CRUD operations
- `UserDB` - User management (optional)

#### ml_models.py
Machine Learning components:
- `ComplaintPrioritizer` - Priority scoring
- `categorize_complaint()` - Auto-categorization
- `find_similar_complaints()` - Duplicate detection
- `calculate_frequency_boost()` - Area-based priority boost

#### utils.py
Helper functions:
- File upload handling
- Date formatting
- Distance calculation
- Badge color mapping

### Frontend Files

#### templates/index.html
Citizen interface featuring:
- Responsive complaint form
- Image upload with preview
- Interactive map with location picker
- Real-time validation
- Success modal with duplicate warnings

#### templates/admin.html
Administrative interface with:
- Statistics cards (Total, Pending, In Progress, Resolved)
- Charts (Category distribution, Priority breakdown)
- Complaint filtering
- Status update functionality
- Detailed complaint view

#### templates/map.html
Map visualization:
- All complaints on interactive map
- Color-coded priority markers
- Marker clustering
- Legend and statistics
- Popup details

#### static/css/style.css
Comprehensive styling:
- CSS Grid and Flexbox layouts
- Responsive design
- Custom color scheme
- Animations and transitions
- Badge and button styles
- Modal designs

#### static/js/main.js
Complaint form functionality:
- Leaflet.js map integration
- Geolocation API
- Image preview
- Form submission with AJAX
- Success modal display

#### static/js/admin.js
Admin dashboard functionality:
- Chart.js integration
- Real-time filtering
- Modal management
- AJAX status updates
- Auto-refresh every 30s

#### static/js/map.js
Map view functionality:
- Marker clustering
- Custom colored markers
- Detailed popups
- Statistics calculation
- URL parameter handling

## Configuration Files

### .env.example
Template for environment variables:
```
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
FLASK_SECRET_KEY=your_secret_key_here
FLASK_ENV=development
MAX_FILE_SIZE=5242880
UPLOAD_FOLDER=static/uploads
```

### requirements.txt
Python dependencies:
- Flask & Flask-CORS
- Supabase client
- ML libraries (scikit-learn, NLTK)
- Image processing (Pillow)
- Geolocation (geopy)

### .gitignore
Excludes:
- Virtual environment
- `.env` file
- Uploaded images
- Python cache
- IDE files

## Database Schema

### complaints table
```sql
- id (BIGSERIAL PRIMARY KEY)
- name, email, phone (Contact info)
- description (TEXT)
- category (VARCHAR)
- priority, priority_score (VARCHAR, INTEGER)
- status (VARCHAR)
- department (VARCHAR)
- latitude, longitude (DECIMAL)
- address (TEXT)
- image_url (TEXT)
- is_duplicate, similar_count (BOOLEAN, INTEGER)
- admin_notes (TEXT)
- created_at, updated_at (TIMESTAMP)
```

## ML Algorithm Details

### Priority Scoring (0-100 points)

1. **Keyword Analysis (40 points)**
   - Critical keywords: emergency, danger, accident, death
   - High keywords: damage, problem, broken, leak
   - Medium keywords: need, repair, fix

2. **Category Weight (25 points)**
   - Critical: Road Damage, Water Supply, Sewage, Building
   - High: Streetlight, Waste Management, Transport
   - Medium: Parks, Noise Pollution

3. **Description Detail (15 points)**
   - 50+ words: 15 points
   - 20-50 words: 10 points
   - <20 words: 5 points

4. **Image Evidence (10 points)**
   - With image: 10 points
   - Without: 0 points

5. **Urgency Indicators (10 points)**
   - Contains: urgent, asap, immediately, emergency

6. **Frequency Boost (up to 15 points)**
   - Category frequency: 2 points each
   - Location frequency: 3 points each

### Duplicate Detection

Uses TF-IDF vectorization and cosine similarity:
- Threshold: 0.6 for similarity
- Threshold: 0.85 for duplicates
- Returns top similar complaints

## API Endpoints

### Public Endpoints
- `GET /` - Home page
- `POST /submit-complaint` - Submit complaint
- `GET /map` - Map view

### Admin Endpoints
- `GET /admin` - Dashboard
- `GET /api/complaints` - List all complaints
- `GET /api/complaints/<id>` - Get complaint details
- `POST /api/complaints/<id>/update` - Update complaint
- `GET /api/statistics` - Get statistics

## Security Features

1. **Input Validation**
   - File type checking
   - Size limits (5MB default)
   - SQL injection prevention (via Supabase)

2. **Environment Variables**
   - Credentials in .env
   - Not committed to git

3. **CORS**
   - Configured for cross-origin requests

4. **File Upload**
   - Secure filename generation
   - Extension validation
   - Size limits

## Performance Optimizations

1. **Database**
   - Indexed columns (status, priority, category)
   - Efficient queries with limits

2. **Frontend**
   - CDN for libraries
   - Marker clustering on map
   - Lazy loading

3. **Caching**
   - Static file caching
   - Browser caching headers

## Deployment Considerations

### Production Checklist
- [ ] Set FLASK_ENV=production
- [ ] Use strong SECRET_KEY
- [ ] Enable HTTPS
- [ ] Set up proper logging
- [ ] Add authentication
- [ ] Implement rate limiting
- [ ] Use production WSGI server (Gunicorn)
- [ ] Set up database backups
- [ ] Configure CDN for static files
- [ ] Add monitoring and analytics

### Environment-Specific Settings
```python
if os.getenv('FLASK_ENV') == 'production':
    DEBUG = False
    TESTING = False
else:
    DEBUG = True
    TESTING = True
```

## Testing Strategy

### Manual Testing
1. Submit various complaint types
2. Test all priority levels
3. Verify duplicate detection
4. Check admin updates
5. Test map functionality

### Unit Testing (Future)
- Test ML scoring
- Test categorization
- Test API endpoints
- Test database operations

## Future Enhancements

1. **Authentication**
   - User login/registration
   - Role-based access control
   - OAuth integration

2. **Notifications**
   - Email notifications
   - SMS alerts
   - Push notifications

3. **Analytics**
   - Advanced reporting
   - Predictive analytics
   - Trend analysis

4. **Mobile App**
   - React Native/Flutter
   - Offline support
   - Camera integration

5. **AI Improvements**
   - Image recognition
   - Severity detection from images
   - Automated routing
   - Sentiment analysis

6. **Integration**
   - Government systems
   - Payment gateways (for fines)
   - GIS systems
   - IoT sensors
