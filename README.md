# Crowdsourced Civic Issue Reporting and Resolution System

A web-based, AI-assisted platform for reporting and resolving civic issues using Flask, Machine Learning, and Supabase.

## 🎯 Features

- **Citizen Reporting Interface**
  - Submit complaints with image evidence
  - Interactive map-based location selection
  - Auto-detect current location
  - Real-time form validation

- **AI-Powered Prioritization**
  - Machine learning-based complaint prioritization
  - Automatic categorization using NLP
  - Duplicate detection and clustering
  - Severity analysis from descriptions

- **Admin Dashboard**
  - Real-time complaint visualization
  - Interactive charts and statistics
  - Department-wise routing
  - Status tracking and updates

- **Interactive Map View**
  - Visualize all complaints on a map
  - Marker clustering for better performance
  - Color-coded priority markers
  - Detailed popup information

## 🚀 Technologies Used

- **Backend**: Flask (Python)
- **Database**: Supabase (PostgreSQL)
- **Frontend**: HTML5, CSS3, JavaScript
- **Maps**: Leaflet.js with OpenStreetMap
- **Charts**: Chart.js
- **ML/NLP**: scikit-learn, NLTK
- **Styling**: Custom CSS with responsive design

## 📋 Prerequisites

- Python 3.8 or higher
- Supabase account (free tier available)
- Modern web browser
- Internet connection for map tiles

## 🛠️ Installation

### 1. Clone or Download the Project

```bash
cd "c:\Users\msant\OneDrive\Documents\New folder (2)"
```

### 2. Create Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download NLTK Data (for ML features)

```bash
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
```

### 5. Set Up Supabase

1. Create a free account at [https://supabase.com](https://supabase.com)
2. Create a new project
3. Go to SQL Editor and run the schema from `SUPABASE_SETUP.md`
4. Get your credentials from Settings > API

### 6. Configure Environment Variables

Copy the example environment file:

```bash
copy .env.example .env
```

Edit `.env` and add your credentials:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-key-here
FLASK_SECRET_KEY=your-random-secret-key
FLASK_ENV=development
```

### 7. Create Required Directories

```bash
mkdir static\uploads
mkdir models
```

## ▶️ Running the Application

### Development Mode

```bash
python app.py
```

The application will be available at: `http://localhost:5000`

### Production Mode

For production deployment:

```bash
# Using Gunicorn (Linux/Mac)
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# On Windows, use waitress
pip install waitress
waitress-serve --host 0.0.0.0 --port 5000 app:app
```

## 📱 Usage

### For Citizens

1. Navigate to `http://localhost:5000`
2. Fill in your personal information
3. Select or auto-detect location on the map
4. Choose complaint category or let AI auto-detect
5. Provide detailed description
6. Upload image evidence (optional)
7. Submit complaint
8. Receive complaint ID and priority level

### For Administrators

1. Navigate to `http://localhost:5000/admin`
2. View real-time statistics and charts
3. Filter complaints by status, priority, or category
4. Click on complaints to view details
5. Update complaint status and add notes
6. View complaints on map

## 🗺️ Map View

Navigate to `http://localhost:5000/map` to see:
- All complaints visualized on an interactive map
- Color-coded markers by priority
- Marker clustering for dense areas
- Detailed popups with complaint information

## 🤖 ML Features

### Priority Calculation

The system uses multiple factors to calculate priority scores (0-100):

1. **Keyword Analysis (40 points)**: Critical, high, medium priority keywords
2. **Category Weight (25 points)**: Infrastructure vs. maintenance issues
3. **Description Detail (15 points)**: Length and completeness
4. **Image Evidence (10 points)**: Visual proof provided
5. **Urgency Indicators (10 points)**: Explicit urgency words
6. **Frequency Boost (15 points)**: Similar complaints in area

### Auto-Categorization

Uses keyword matching to automatically categorize complaints into:
- Road Damage
- Waste Management
- Streetlight
- Water Supply
- Sewage
- Parks & Gardens
- Public Transport
- Building Safety
- Noise Pollution
- Other

### Duplicate Detection

Uses TF-IDF vectorization and cosine similarity to:
- Detect similar complaints
- Link related issues
- Reduce redundant processing

## 📊 Database Schema

See `SUPABASE_SETUP.md` for complete schema documentation.

### Main Tables

- **complaints**: Stores all complaint data
- **users**: Stores user information (optional)

## 🎨 Customization

### Changing Categories

Edit `config.py`:

```python
CATEGORIES = [
    'Your Category 1',
    'Your Category 2',
    # Add more...
]
```

### Adjusting Priority Weights

Edit `ml_models.py` in the `calculate_priority_score` method to adjust scoring weights.

### Styling

Modify `static/css/style.css` to change colors, fonts, and layout.

## 🌐 Deployment

### Heroku

```bash
# Install Heroku CLI
heroku create your-app-name
heroku config:set SUPABASE_URL=your-url
heroku config:set SUPABASE_KEY=your-key
git push heroku main
```

### Render

1. Connect your GitHub repository
2. Set environment variables in dashboard
3. Deploy automatically on push

### Traditional VPS

1. Use Nginx as reverse proxy
2. Set up SSL with Let's Encrypt
3. Use systemd for process management
4. Configure Gunicorn with supervisor

## 🐛 Troubleshooting

### Map Not Loading
- Check internet connection
- Ensure Leaflet.js CDN is accessible
- Check browser console for errors

### Database Connection Issues
- Verify Supabase credentials
- Check if tables are created
- Ensure RLS policies are set correctly

### ML Features Not Working
- Download NLTK data
- Check Python version (3.8+)
- Install all requirements

## 📝 API Endpoints

- `GET /` - Home page (complaint form)
- `POST /submit-complaint` - Submit new complaint
- `GET /admin` - Admin dashboard
- `GET /map` - Map view
- `GET /api/complaints` - Get all complaints (JSON)
- `GET /api/complaints/<id>` - Get specific complaint
- `POST /api/complaints/<id>/update` - Update complaint
- `GET /api/statistics` - Get statistics

## 🔒 Security Considerations

- Never commit `.env` file
- Use strong secret keys
- Enable HTTPS in production
- Implement rate limiting
- Add authentication for admin panel
- Validate all user inputs
- Sanitize file uploads

## 📄 License

This project is open-source and available for educational purposes.

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📧 Support

For issues and questions:
- Check existing issues
- Create a new issue with detailed description
- Include error messages and screenshots

## 🎓 Project Information

**Organization**: Government of Jharkhand  
**Department**: Department of Higher and Technical Education  
**Project ID**: 2S031  
**Theme**: Clean & Green Technology

---

**Note**: This is a demonstration project. For production use, implement proper authentication, authorization, and additional security measures.
