# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Python Dependencies

Open PowerShell in this folder and run:

```powershell
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Download NLTK Data

```powershell
python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
```

### Step 3: Set Up Supabase Database

1. Go to [https://supabase.com](https://supabase.com) and create a free account
2. Create a new project (choose a name and password)
3. Wait for the project to initialize (2-3 minutes)
4. Go to **SQL Editor** (left sidebar)
5. Click **New Query**
6. Copy and paste the SQL from `SUPABASE_SETUP.md`
7. Click **Run** to create tables

### Step 4: Get Your Supabase Credentials

1. In Supabase, go to **Settings** > **API** (left sidebar)
2. Copy the **Project URL** (looks like: https://xxxxx.supabase.co)
3. Copy the **anon public** key (under Project API keys)

### Step 5: Configure Environment

1. Copy `.env.example` to `.env`:
   ```powershell
   Copy-Item .env.example .env
   ```

2. Edit `.env` file with your credentials:
   ```
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-anon-key-here
   FLASK_SECRET_KEY=my-super-secret-key-12345
   FLASK_ENV=development
   ```

### Step 6: Run the Application

```powershell
python app.py
```

Open your browser and go to: **http://localhost:5000**

## 📱 Testing the Application

### Test Citizen Portal
1. Go to http://localhost:5000
2. Fill in the form with sample data
3. Click "Use My Current Location" or click on the map
4. Select a category or use "Auto-Detect"
5. Write a detailed description (use words like "urgent", "emergency", "critical" for higher priority)
6. Upload an image (optional)
7. Click Submit

### Test Admin Dashboard
1. Go to http://localhost:5000/admin
2. View statistics and charts
3. Click on complaint rows to view details
4. Click edit icon to update status
5. Use filters to filter by status/priority/category

### Test Map View
1. Go to http://localhost:5000/map
2. See all complaints on the map
3. Click markers to see details
4. Use legend to understand priority colors

## 🎯 Sample Test Data

### High Priority Complaint
- **Description**: "Emergency! Large pothole on Main Road causing accidents. Multiple vehicles damaged. Immediate repair needed!"
- **Category**: Road Damage
- **Expected Priority**: Critical/High

### Medium Priority Complaint
- **Description**: "Street light not working on Park Street for 3 days"
- **Category**: Streetlight
- **Expected Priority**: Medium

### Low Priority Complaint
- **Description**: "Need to clean the park garden"
- **Category**: Parks & Gardens
- **Expected Priority**: Low

## 🔧 Troubleshooting

### "Module not found" errors
```powershell
pip install -r requirements.txt
```

### Database connection errors
- Check your SUPABASE_URL and SUPABASE_KEY in .env
- Make sure you ran the SQL schema
- Verify internet connection

### Map not loading
- Check internet connection (maps use OpenStreetMap tiles)
- Try refreshing the page
- Check browser console for errors

### Port 5000 already in use
```powershell
# Use a different port
python app.py
# Or kill the process using port 5000
```

## 📊 Understanding Priority Scores

The ML model assigns priority based on:

1. **Keywords** (40 pts): 
   - Critical: emergency, danger, accident, severe
   - High: damage, problem, broken, leak
   - Medium: need, repair, fix

2. **Category** (25 pts):
   - Critical categories: Road, Water, Sewage, Building
   - High categories: Streetlight, Waste, Transport

3. **Detail Level** (15 pts):
   - More detailed descriptions = higher priority

4. **Image Evidence** (10 pts):
   - Photo evidence increases priority

5. **Urgency Words** (10 pts):
   - Words like "urgent", "immediately", "asap"

6. **Frequency** (15 pts):
   - Multiple complaints in same area/category

**Total Score Range**: 0-100
- 70+: Critical
- 50-69: High
- 30-49: Medium
- 0-29: Low

## 🎨 Customization Tips

### Change Colors
Edit `static/css/style.css` and modify CSS variables:
```css
:root {
    --primary-color: #2563eb;  /* Change to your color */
    --secondary-color: #64748b;
}
```

### Add New Categories
Edit `config.py`:
```python
CATEGORIES = [
    'Road Damage',
    'Your New Category',  # Add here
    ...
]
```

### Adjust Priority Algorithm
Edit `ml_models.py` in `calculate_priority_score()` method to change scoring weights.

## 🌐 Next Steps

1. **Add Authentication**: Implement login for admin panel
2. **Email Notifications**: Send emails on complaint submission/updates
3. **SMS Integration**: Add SMS alerts for critical issues
4. **Mobile App**: Create React Native/Flutter mobile app
5. **Advanced ML**: Train custom ML models on historical data
6. **Analytics**: Add more detailed analytics and reports

## 📞 Need Help?

Check:
- README.md for detailed documentation
- SUPABASE_SETUP.md for database setup
- Browser console for JavaScript errors
- Terminal for Python errors

---

**Happy Coding! 🎉**
