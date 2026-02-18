# Deployment Guide

## 🌐 Production Deployment Options

### Option 1: Heroku (Easiest for Beginners)

#### Prerequisites
- Heroku account (free tier available)
- Git installed
- Heroku CLI installed

#### Steps

1. **Install Heroku CLI**
```bash
# Windows (using Chocolatey)
choco install heroku-cli

# Or download from https://devcenter.heroku.com/articles/heroku-cli
```

2. **Login to Heroku**
```bash
heroku login
```

3. **Create Heroku App**
```bash
heroku create civic-issue-app-your-name
```

4. **Add Procfile**
Create `Procfile` in project root:
```
web: gunicorn app:app
```

5. **Set Environment Variables**
```bash
heroku config:set SUPABASE_URL=https://your-project.supabase.co
heroku config:set SUPABASE_KEY=your-anon-key
heroku config:set FLASK_SECRET_KEY=your-production-secret-key
heroku config:set FLASK_ENV=production
```

6. **Deploy**
```bash
git init
git add .
git commit -m "Initial commit"
git push heroku main
```

7. **Open Your App**
```bash
heroku open
```

**Cost:** Free tier available (with limitations)

---

### Option 2: Render (Modern Alternative)

#### Prerequisites
- Render account (free tier available)
- GitHub account
- Git repository

#### Steps

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/civic-issue-app.git
git push -u origin main
```

2. **Create Web Service on Render**
- Go to https://render.com
- Click "New +" > "Web Service"
- Connect GitHub repository
- Configure:
  - **Name:** civic-issue-app
  - **Environment:** Python 3
  - **Build Command:** `pip install -r requirements.txt`
  - **Start Command:** `gunicorn app:app`

3. **Add Environment Variables**
In Render dashboard:
- SUPABASE_URL
- SUPABASE_KEY
- FLASK_SECRET_KEY
- FLASK_ENV=production

4. **Deploy**
- Click "Create Web Service"
- Render will auto-deploy on every git push

**Cost:** Free tier available (0.1 CPU, 512MB RAM)

---

### Option 3: Railway (Fast & Easy)

#### Steps

1. **Install Railway CLI**
```bash
npm install -g @railway/cli
```

2. **Login**
```bash
railway login
```

3. **Initialize Project**
```bash
railway init
```

4. **Add Environment Variables**
```bash
railway variables set SUPABASE_URL=https://your-project.supabase.co
railway variables set SUPABASE_KEY=your-anon-key
railway variables set FLASK_SECRET_KEY=your-secret-key
railway variables set FLASK_ENV=production
```

5. **Deploy**
```bash
railway up
```

**Cost:** Free tier with $5 credit/month

---

### Option 4: DigitalOcean App Platform

#### Steps

1. **Push to GitHub** (as in Option 2)

2. **Create App**
- Go to https://cloud.digitalocean.com
- Click "Create" > "Apps"
- Connect GitHub repo
- Configure:
  - **Type:** Web Service
  - **Build Command:** `pip install -r requirements.txt`
  - **Run Command:** `gunicorn --worker-tmp-dir /dev/shm app:app`

3. **Set Environment Variables** in dashboard

4. **Deploy** automatically

**Cost:** Basic plan starts at $5/month

---

### Option 5: Traditional VPS (DigitalOcean, Linode, AWS EC2)

For production environments with full control.

#### Prerequisites
- Ubuntu 22.04 VPS
- Domain name (optional)
- SSH access

#### Steps

1. **Connect to Server**
```bash
ssh root@your-server-ip
```

2. **Update System**
```bash
apt update && apt upgrade -y
```

3. **Install Python and Dependencies**
```bash
apt install python3 python3-pip python3-venv nginx git -y
```

4. **Create Application User**
```bash
adduser civicapp
usermod -aG sudo civicapp
su - civicapp
```

5. **Clone Repository**
```bash
cd /home/civicapp
git clone https://github.com/yourusername/civic-issue-app.git
cd civic-issue-app
```

6. **Set Up Python Environment**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

7. **Configure Environment**
```bash
cp .env.example .env
nano .env
# Edit with your production credentials
```

8. **Test Application**
```bash
gunicorn --bind 0.0.0.0:8000 app:app
# Press Ctrl+C after testing
```

9. **Create Systemd Service**
```bash
sudo nano /etc/systemd/system/civicapp.service
```

Add:
```ini
[Unit]
Description=Civic Issue Reporting App
After=network.target

[Service]
User=civicapp
Group=www-data
WorkingDirectory=/home/civicapp/civic-issue-app
Environment="PATH=/home/civicapp/civic-issue-app/venv/bin"
ExecStart=/home/civicapp/civic-issue-app/venv/bin/gunicorn --workers 3 --bind unix:civicapp.sock -m 007 app:app

[Install]
WantedBy=multi-user.target
```

10. **Start Service**
```bash
sudo systemctl start civicapp
sudo systemctl enable civicapp
sudo systemctl status civicapp
```

11. **Configure Nginx**
```bash
sudo nano /etc/nginx/sites-available/civicapp
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/civicapp/civic-issue-app/civicapp.sock;
    }

    location /static {
        alias /home/civicapp/civic-issue-app/static;
    }

    client_max_body_size 5M;
}
```

12. **Enable Site**
```bash
sudo ln -s /etc/nginx/sites-available/civicapp /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

13. **Configure Firewall**
```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
```

14. **Set Up SSL with Let's Encrypt**
```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

15. **Set Up Auto-Renewal**
```bash
sudo certbot renew --dry-run
```

**Cost:** $5-10/month for basic VPS

---

### Option 6: Docker Deployment

#### Create Dockerfile

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p static/uploads models

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

#### Create docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_KEY=${SUPABASE_KEY}
      - FLASK_SECRET_KEY=${FLASK_SECRET_KEY}
      - FLASK_ENV=production
    volumes:
      - ./static/uploads:/app/static/uploads
    restart: unless-stopped
```

#### Deploy

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## 🔒 Security Checklist for Production

### Before Deployment

- [ ] Change FLASK_SECRET_KEY to strong random value
- [ ] Set FLASK_ENV=production
- [ ] Enable HTTPS/SSL
- [ ] Set up firewall rules
- [ ] Configure CORS properly
- [ ] Add rate limiting
- [ ] Implement authentication for admin
- [ ] Set up database backups
- [ ] Configure error logging
- [ ] Add monitoring

### Generate Strong Secret Key

```python
import secrets
print(secrets.token_hex(32))
```

### Add Rate Limiting

Install Flask-Limiter:
```bash
pip install Flask-Limiter
```

Update app.py:
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/submit-complaint', methods=['POST'])
@limiter.limit("10 per hour")
def submit_complaint():
    # existing code
```

---

## 📊 Monitoring & Logging

### Set Up Logging

Update app.py:
```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    file_handler = RotatingFileHandler('logs/civicapp.log', 
                                      maxBytes=10240, 
                                      backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    
    app.logger.setLevel(logging.INFO)
    app.logger.info('Civic App startup')
```

### Use Monitoring Services

#### Sentry (Error Tracking)
```bash
pip install sentry-sdk[flask]
```

```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="your-sentry-dsn",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)
```

#### Uptime Monitoring
- UptimeRobot (free)
- Pingdom
- StatusCake

---

## 🔄 Continuous Deployment

### GitHub Actions

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Deploy to Heroku
      uses: akhileshns/heroku-deploy@v3.12.12
      with:
        heroku_api_key: ${{secrets.HEROKU_API_KEY}}
        heroku_app_name: "your-app-name"
        heroku_email: "your-email@example.com"
```

---

## 📈 Performance Optimization

### Enable Caching

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/api/statistics')
@cache.cached(timeout=300)  # Cache for 5 minutes
def get_statistics():
    # existing code
```

### Use CDN for Static Files

Options:
- Cloudflare CDN
- Amazon CloudFront
- KeyCDN

### Database Optimization

- Add indexes (already in schema)
- Use connection pooling
- Implement pagination for large datasets

---

## 🧪 Pre-Deployment Testing

```bash
# Test with production settings locally
FLASK_ENV=production python app.py

# Load testing with Apache Bench
ab -n 1000 -c 10 http://localhost:5000/

# Security scan
pip install safety
safety check
```

---

## 📱 Domain Configuration

### Point Domain to Server

Add DNS A records:
```
Type: A
Name: @
Value: your-server-ip

Type: A
Name: www
Value: your-server-ip
```

### Configure in Nginx

Update server_name in Nginx config:
```nginx
server_name yourdomain.com www.yourdomain.com;
```

---

## 💾 Backup Strategy

### Database Backups

Supabase handles automatic backups, but you can also:

```bash
# Manual backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -h db.supabase.co -U postgres -d your_db > backup_$DATE.sql
```

### File Backups

```bash
# Backup uploads folder
tar -czf uploads_backup_$(date +%Y%m%d).tar.gz static/uploads/
```

---

## 🎯 Post-Deployment Checklist

- [ ] Test all features in production
- [ ] Monitor error logs
- [ ] Check performance metrics
- [ ] Verify SSL certificate
- [ ] Test on mobile devices
- [ ] Set up automated backups
- [ ] Configure monitoring alerts
- [ ] Update documentation
- [ ] Train users
- [ ] Plan maintenance schedule

---

## 📞 Troubleshooting

### Common Issues

1. **500 Internal Server Error**
   - Check logs: `tail -f /var/log/nginx/error.log`
   - Verify environment variables
   - Check Python errors in app logs

2. **Static Files Not Loading**
   - Check Nginx static file configuration
   - Verify file permissions
   - Clear browser cache

3. **Database Connection Failed**
   - Verify Supabase credentials
   - Check network connectivity
   - Ensure tables exist

4. **High Memory Usage**
   - Reduce Gunicorn workers
   - Implement caching
   - Optimize queries

---

## 🌟 Recommended Production Stack

**Optimal Setup:**
- **Hosting:** DigitalOcean Droplet ($12/month)
- **Database:** Supabase (Free tier sufficient)
- **CDN:** Cloudflare (Free)
- **Monitoring:** Sentry (Free tier)
- **Uptime:** UptimeRobot (Free)
- **Email:** SendGrid (Free tier)
- **Total Cost:** ~$12/month

This setup provides excellent performance, reliability, and scalability for a civic reporting system.
