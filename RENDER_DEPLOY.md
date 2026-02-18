# 🚀 Render Deployment Guide

## ✅ Why Render is Better for Your Flask App

- ✅ **Full Flask support** (not serverless)
- ✅ **ML models** work perfectly
- ✅ **Persistent storage** for uploads
- ✅ **750 hours/month** free
- ✅ **Auto-deploy** from GitHub
- ✅ **No configuration headaches**

---

## 📦 Step 1: Prerequisites

✅ Your code is already on GitHub: `https://github.com/santosh5133j6/civic-complaint-system-`
✅ `render.yaml` configuration created
✅ All dependencies in `requirements.txt`

---

## 🌐 Step 2: Deploy to Render

### 1. **Go to Render**
Visit: https://render.com

### 2. **Sign Up / Sign In**
- Click **"Get Started"** or **"Sign In"**
- Choose **"Sign in with GitHub"**
- Authorize Render to access your GitHub

### 3. **Create New Web Service**
- Click **"New +"** in the top right
- Select **"Web Service"**

### 4. **Connect Repository**
- Find and select: `santosh5133j6/civic-complaint-system-`
- Click **"Connect"**

### 5. **Configure Service**
Fill in these settings:

**Name:** `civic-complaint-system` (or any name you like)

**Region:** Choose closest to you (e.g., `Oregon (US West)`)

**Branch:** `main`

**Runtime:** `Python 3`

**Build Command:** 
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
gunicorn app:app --bind 0.0.0.0:$PORT
```

**Instance Type:** `Free`

### 6. **Add Environment Variables** (CRITICAL!)

Scroll down to **"Environment Variables"** section and click **"Add Environment Variable"**. Add these THREE variables:

| Key | Value |
|-----|-------|
| `SUPABASE_URL` | `https://wdncfyaeijhdamlxulko.supabase.co` |
| `SUPABASE_KEY` | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndkbmNmeWFlaWpoZGFtbHh1bGtvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Njk0Mzc4NjksImV4cCI6MjA4NTAxMzg2OX0.bL4L9GIy5X1_GQC81oZOF8UzoTlqjlxFN0E5hC-ZDT0` |
| `SECRET_KEY` | `flask-prod-civic-2026-secure-key-xyz789` |

**⚠️ Important:** Change `SECRET_KEY` to your own random string!

### 7. **Deploy!**
Click **"Create Web Service"** at the bottom

---

## ⏱️ Wait for Deployment

- **Initial deployment**: 3-5 minutes
- **Status**: Watch the logs in real-time
- **Success**: You'll see "Your service is live 🎉"

---

## 🌍 Access Your App

After deployment completes, Render will give you a URL like:
```
https://civic-complaint-system.onrender.com
```

**That's it!** Your app is now live! 🎉

---

## 🔄 Future Updates

Whenever you update your code:

```bash
cd C:\Projects\civic-complaint-system
git add .
git commit -m "Updated feature XYZ"
git push origin main
```

**Render automatically redeploys!** No manual steps needed! ✨

---

## ⚙️ Post-Deployment Setup

### Update Supabase CORS

1. Go to Supabase Dashboard: https://supabase.com/dashboard
2. Select your project: `wdncfyaeijhdamlxulko`
3. Settings → API → CORS Allowed Origins
4. Add your Render URL: `https://civic-complaint-system.onrender.com`

### Update Storage CORS

1. Supabase Dashboard → Storage → Settings
2. CORS Configuration:
```json
[
  {
    "origin": "https://civic-complaint-system.onrender.com",
    "methods": ["GET", "POST", "PUT", "DELETE"],
    "headers": ["*"]
  }
]
```

---

## 🐛 Troubleshooting

### App shows "Service Unavailable"
**Solution**: Wait 2-3 minutes for initial deployment. Check logs for errors.

### Missing packages error
**Solution**: Ensure all packages in `requirements.txt`. Redeploy.

### Database connection error
**Solution**: Verify environment variables are set correctly in Render dashboard.

### App sleeps after inactivity (Free tier)
**Expected**: Free tier apps sleep after 15 minutes of inactivity. First request after sleep takes ~30 seconds to wake up.

---

## 📊 Monitor Your App

**Render Dashboard provides:**
- ✅ **Real-time logs**
- ✅ **Metrics** (CPU, memory, requests)
- ✅ **Deployment history**
- ✅ **Auto-deploy settings**
- ✅ **Custom domain** (if you have one)

---

## 💰 Free Tier Limits

**Render Free Tier:**
- ✅ 750 hours/month (enough for 1 app running 24/7)
- ✅ 512 MB RAM
- ✅ Shared CPU
- ✅ Auto-sleep after 15 min inactivity
- ✅ Custom domains
- ✅ Automatic SSL

More than enough for your civic complaint system! 🎯

---

## 🎯 Quick Setup Checklist

- [ ] Sign up at https://render.com
- [ ] Connect GitHub repository
- [ ] Create Web Service
- [ ] Set Runtime to Python 3
- [ ] Add build command: `pip install -r requirements.txt`
- [ ] Add start command: `gunicorn app:app --bind 0.0.0.0:$PORT`
- [ ] Add 3 environment variables (SUPABASE_URL, SUPABASE_KEY, SECRET_KEY)
- [ ] Click "Create Web Service"
- [ ] Wait 3-5 minutes
- [ ] Access your live app URL!
- [ ] Update Supabase CORS settings

---

## 🎉 You're Live!

Your civic complaint system is now:
- ✅ **Deployed** on Render
- ✅ **Auto-scales** as needed
- ✅ **Secure** with HTTPS
- ✅ **Auto-deploys** on git push
- ✅ **Monitored** with logs

Share your URL and start collecting complaints! 🚀

---

## 🆘 Need Help?

**Render Docs:** https://render.com/docs
**Your Dashboard:** https://dashboard.render.com
**Support:** https://render.com/support

---

**Deployment Time: ~5 minutes** | **Cost: $0/month (Free tier)** | **Difficulty: Easy** ⭐⭐⭐⭐⭐
