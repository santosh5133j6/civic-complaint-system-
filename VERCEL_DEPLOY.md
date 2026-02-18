# 🚀 Vercel Deployment Guide

## Prerequisites
- GitHub account
- Vercel account (free) - https://vercel.com
- Git installed on your computer

## 📦 Step 1: Prepare Your Project

Your project is already configured with:
- ✅ `vercel.json` - Vercel configuration
- ✅ `api/index.py` - Serverless entry point
- ✅ `requirements.txt` - Python dependencies
- ✅ `.gitignore` - Excludes sensitive files

## 🔐 Step 2: Protect Sensitive Data

**IMPORTANT**: Never commit your `.env` file!

Your `.env` file is already in `.gitignore`, but double-check:
```bash
# Make sure these are NOT committed:
.env
__pycache__/
.vercel
```

## 📤 Step 3: Push to GitHub

### If you haven't initialized Git yet:
```bash
# Navigate to your project folder
cd "C:\Users\msant\OneDrive\Documents\New folder (2)"

# Initialize Git
git init

# Add all files
git add .

# Make first commit
git commit -m "Initial commit - Civic Complaint System"

# Create GitHub repository at https://github.com/new
# Then connect and push:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### If Git is already initialized:
```bash
git add .
git commit -m "Prepared for Vercel deployment"
git push origin main
```

## 🌐 Step 4: Deploy to Vercel

### Option A: Via Vercel Dashboard (Easiest)

1. **Go to Vercel**: https://vercel.com
2. **Sign in** with GitHub
3. **Click "Add New Project"**
4. **Import your GitHub repository**
5. **Configure Project**:
   - Framework Preset: **Other**
   - Root Directory: `./` (leave as is)
   - Build Command: (leave empty)
   - Output Directory: (leave empty)

6. **Add Environment Variables** (CRITICAL!):
   - Click "Environment Variables"
   - Add these:
     ```
     SUPABASE_URL = https://wdncfyaeijhdamlxulko.supabase.co
     SUPABASE_KEY = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndkbmNmeWFlaWpoZGFtbHh1bGtvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njk0Mzc4NjksImV4cCI6MjA4NTAxMzg2OX0.bL4L9GIy5X1_GQC81oZOF8UzoTlqjlxFN0E5hC-ZDT0
     SECRET_KEY = your-super-secret-key-here-change-this
     FLASK_ENV = production
     ```
   - Make sure to apply to **Production**, **Preview**, and **Development**

7. **Click "Deploy"** - Vercel will build and deploy! 🎉

### Option B: Via Vercel CLI

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel

# Follow prompts, then add environment variables:
vercel env add SUPABASE_URL
vercel env add SUPABASE_KEY
vercel env add SECRET_KEY

# Redeploy with env vars
vercel --prod
```

## 🔄 Step 5: Future Updates

Whenever you want to update your deployed app:

```bash
# Make your changes to code
# ...

# Commit and push
git add .
git commit -m "Updated feature XYZ"
git push origin main

# Vercel automatically redeploys! ✨
```

That's it! Every push to `main` branch triggers automatic redeployment.

## 🌍 Access Your App

After deployment, Vercel provides:
- **Production URL**: `https://your-project-name.vercel.app`
- **Preview URLs**: For each branch/PR
- **Auto SSL**: Free HTTPS certificate

## ⚙️ Post-Deployment Configuration

### 1. Update Supabase Storage CORS

Go to Supabase Dashboard → Storage → Settings → CORS:
```json
[
  {
    "origin": "https://your-project-name.vercel.app",
    "methods": ["GET", "POST", "PUT", "DELETE"],
    "headers": ["*"]
  }
]
```

### 2. Custom Domain (Optional)

In Vercel Dashboard → Project → Settings → Domains:
- Add your custom domain
- Update DNS records as instructed

## 🐛 Troubleshooting

### Issue: "Module not found"
**Solution**: Make sure all imports are in `requirements.txt`

### Issue: "500 Internal Server Error"
**Solution**: Check Vercel logs:
1. Go to Vercel Dashboard
2. Click on your deployment
3. View "Functions" tab for error logs

### Issue: Environment variables not working
**Solution**: 
1. Vercel Dashboard → Project → Settings → Environment Variables
2. Make sure variables are set for all environments
3. Redeploy: `vercel --prod`

### Issue: Static files not loading
**Solution**: Already configured in `vercel.json` with static route

### Issue: File uploads not persisting
**Note**: Vercel's serverless functions are stateless. For persistent uploads:
- Use Supabase Storage (already configured in your app)
- Files uploaded to Supabase will persist across deployments

## 📊 Monitoring

Vercel provides built-in monitoring:
- **Analytics**: https://vercel.com/docs/analytics
- **Logs**: Real-time function logs
- **Performance**: Core Web Vitals tracking

## 💰 Vercel Free Tier Limits

- ✅ Unlimited deployments
- ✅ 100 GB bandwidth/month
- ✅ 100 GB-hours serverless function execution
- ✅ Automatic SSL
- ✅ Custom domains

More than enough for most projects!

## 🎯 Quick Commands Reference

```bash
# Deploy to production
vercel --prod

# View deployment
vercel ls

# View logs
vercel logs

# Remove deployment
vercel remove your-project-name
```

## ✅ Checklist

Before going live:
- [ ] Pushed code to GitHub
- [ ] Added environment variables in Vercel
- [ ] Tested deployment URL
- [ ] Updated Supabase CORS settings
- [ ] Changed default admin password
- [ ] Verified image uploads work
- [ ] Tested all features on production URL

## 🎉 You're Live!

Your civic complaint system is now deployed and accessible worldwide at:
`https://your-project-name.vercel.app`

Share this URL with users and watch the complaints roll in! 🚀
