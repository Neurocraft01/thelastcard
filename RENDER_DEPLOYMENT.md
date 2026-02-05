# 🚀 Render Deployment Guide - The Last Card ($7 Starter Plan)

## 📋 Prerequisites

- ✅ GitHub account with your repository pushed
- ✅ Render account (sign up at https://render.com)
- ✅ Neon PostgreSQL database URL (or use Render's free PostgreSQL)
- ✅ Gmail account for email sending

---

## 🎯 Quick Deploy Steps

### 1️⃣ Prepare Your Repository

Make sure these files are in your repository:
- ✅ `build.sh` - Build script
- ✅ `render.yaml` - Render configuration
- ✅ `.renderignore` - Files to exclude
- ✅ `requirements.txt` - Python dependencies
- ✅ Health check endpoint at `/healthz`

Make `build.sh` executable:
```bash
git update-index --chmod=+x build.sh
git add build.sh
git commit -m "Make build.sh executable"
git push
```

---

### 2️⃣ Create New Web Service on Render

1. **Go to Render Dashboard**: https://dashboard.render.com/
2. **Click "New +"** → **Web Service**
3. **Connect your GitHub repository**: `thelastcard` or your repo name
4. **Configure the service**:

#### Basic Configuration:
```
Name: thelastcard-web
Region: Oregon (or closest to your users)
Branch: main
Runtime: Python 3
```

#### Build Configuration:
```
Build Command: ./build.sh
Start Command: gunicorn nfc_platform.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120
```

#### Plan Selection:
```
Instance Type: Starter ($7/month)
```

---

### 3️⃣ Set Up Environment Variables

Click **"Advanced"** and add these environment variables:

#### Required Variables:

```env
# Django Settings
DEBUG=False
PYTHON_VERSION=3.12.2

# Security - Generate a new secret key
SECRET_KEY=your-super-secret-key-min-50-chars-CHANGE-THIS

# Database - Use Neon or Render PostgreSQL
DATABASE_URL=postgresql://user:password@host/dbname

# Domain Settings - REPLACE WITH YOUR RENDER URL
ALLOWED_HOSTS=thelastcard-web.onrender.com,localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=https://thelastcard-web.onrender.com,http://localhost:8000
SITE_URL=https://thelastcard-web.onrender.com

# Site Configuration
SITE_NAME=The Last Card

# Email Configuration (Gmail SMTP)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=thelastcardnfc@gmail.com
EMAIL_HOST_PASSWORD=zcys rdfo aieo bmla
DEFAULT_FROM_EMAIL=The Last Card <thelastcardnfc@gmail.com>
```

#### 📝 Important Notes:

**Generate a new SECRET_KEY:**
```python
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

**For ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS:**
- Initially use: `thelastcard-web.onrender.com` (or your service name)
- After deployment, Render will show you the actual URL
- Update these variables with the correct URL

---

### 4️⃣ Configure Health Check

In Render dashboard:
```
Health Check Path: /healthz
```

This endpoint checks:
- ✅ Application is running
- ✅ Database connection is working

---

### 5️⃣ Database Configuration

#### Option A: Use Your Existing Neon Database (Recommended)
```env
DATABASE_URL=postgresql://neondb_owner:npg_y8FMp0XVKHLW@ep-dark-wildflower-aizjaibz-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require
```

#### Option B: Create Render PostgreSQL (Free with $7 plan)
1. Click **"New +"** → **PostgreSQL**
2. Name: `thelastcard-db`
3. Plan: **Starter** (Free)
4. Copy the **Internal Database URL**
5. Paste it in `DATABASE_URL` environment variable

---

### 6️⃣ Deploy Configuration

#### Health Check Settings:
```
Health Check Path: /healthz
Health Check Interval: 30 seconds
Health Check Timeout: 10 seconds
```

#### Auto-Deploy Settings:
```
✅ Auto-Deploy: Enabled
Trigger: On every push to main branch
```

#### Build Filters (Optional):
To prevent unnecessary deploys, add these **Ignored Paths**:
```
*.md
design/**
scripts/**
media/**
.vscode/**
```

---

## 🔧 $7 Plan Optimizations

### Performance Tuning for Starter Plan

The $7 Starter plan includes:
- ✅ 512 MB RAM
- ✅ 0.5 CPU
- ✅ Free PostgreSQL database
- ✅ Free SSL certificate
- ✅ Automatic deploys

#### Gunicorn Workers Configuration:
```bash
# Optimized for 512MB RAM
gunicorn nfc_platform.wsgi:application \
  --bind 0.0.0.0:$PORT \
  --workers 2 \
  --threads 4 \
  --timeout 120 \
  --max-requests 1000 \
  --max-requests-jitter 50
```

**Workers Formula**: `(2 x CPU cores) + 1`
- For 0.5 CPU → 2 workers is optimal
- 4 threads per worker handles concurrent requests
- `--max-requests` prevents memory leaks

#### Django Settings for Production:

Already configured in your `settings.py`:
```python
DEBUG = False
SECURE_SSL_REDIRECT = True
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

---

## 📊 Post-Deployment Steps

### 1. Create Superuser

After first successful deploy:
```bash
# Open Shell in Render dashboard
python manage.py createsuperuser
```

Or use the included script:
```bash
python create_admin_users.py
```

### 2. Verify Deployment

Check these URLs:
- ✅ Health Check: `https://your-app.onrender.com/healthz`
- ✅ Admin Panel: `https://your-app.onrender.com/admin/`
- ✅ Landing Page: `https://your-app.onrender.com/`

### 3. Update Environment Variables

After seeing your actual Render URL, update:
```env
ALLOWED_HOSTS=your-actual-app-name.onrender.com
CSRF_TRUSTED_ORIGINS=https://your-actual-app-name.onrender.com
SITE_URL=https://your-actual-app-name.onrender.com
```

### 4. Test Core Features

- ✅ User registration
- ✅ User login
- ✅ Create NFC card
- ✅ View public profile
- ✅ QR code generation
- ✅ Email sending
- ✅ File uploads (logo, profile image)

---

## 🐛 Troubleshooting

### Deployment Fails

**Check Build Logs:**
1. Go to Render Dashboard
2. Click on your service
3. Go to **"Logs"** tab
4. Look for error messages

**Common Issues:**

#### Issue: "Build command failed"
```bash
# Make sure build.sh is executable
chmod +x build.sh
git add build.sh --chmod=+x
git commit -m "Fix build.sh permissions"
git push
```

#### Issue: "Database connection failed"
- ✔️ Check `DATABASE_URL` is correct
- ✔️ Verify database is running
- ✔️ Test connection from health check: `/healthz`

#### Issue: "Static files not loading"
```python
# Verify in settings.py:
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Run collectstatic in shell:
python manage.py collectstatic --no-input
```

#### Issue: "502 Bad Gateway"
- ✔️ Check if Gunicorn is running correctly
- ✔️ Verify `PORT` environment variable is used
- ✔️ Check worker configuration (reduce if needed)

#### Issue: "Out of Memory (OOM)"
Reduce Gunicorn workers:
```bash
# Change to 1 worker if needed
gunicorn nfc_platform.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --threads 4
```

---

## 📈 Monitoring

### Render Dashboard
- **Metrics**: CPU, Memory, Request count
- **Logs**: Real-time application logs
- **Health Checks**: Service availability

### Health Check Endpoint
```bash
curl https://your-app.onrender.com/healthz
```

Response:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

---

## 🔐 Security Checklist

- ✅ `DEBUG = False` in production
- ✅ Strong `SECRET_KEY` (50+ characters)
- ✅ HTTPS enabled (automatic on Render)
- ✅ `SECURE_SSL_REDIRECT = True`
- ✅ Database uses SSL (`sslmode=require`)
- ✅ Environment variables not in code
- ✅ `.env` file in `.gitignore`

---

## 💰 Cost Optimization Tips

### Stay Within $7/month Plan:

1. **Use Render's Free PostgreSQL**
   - Included with Starter plan
   - 1GB storage
   - Sufficient for small-medium apps

2. **Optimize Media Storage**
   - Current: Local file storage (limited)
   - Upgrade option: Cloudflare R2 (already configured in code)
   - Free tier: 10GB storage

3. **Reduce Build Times**
   - Use `.renderignore` to exclude unnecessary files
   - Cache dependencies when possible

4. **Monitor Resource Usage**
   - Check memory usage in Render dashboard
   - Adjust workers if hitting limits
   - Consider upgrading if consistently maxed out

---

## 🔄 Continuous Deployment

### Automatic Deploys

Already configured to deploy on:
- ✅ Every push to `main` branch
- ✅ Environment variable changes
- ✅ Manual deploy trigger

### Manual Deploy

From Render Dashboard:
1. Go to your service
2. Click **"Manual Deploy"**
3. Select **"Deploy latest commit"**

---

## 📚 Additional Resources

- **Render Docs**: https://render.com/docs
- **Django Deployment**: https://docs.djangoproject.com/en/5.0/howto/deployment/
- **Neon Database**: https://neon.tech/docs
- **Gunicorn**: https://docs.gunicorn.org/

---

## ✅ Deployment Checklist

Before going live:

- [ ] All environment variables configured
- [ ] `DEBUG = False`
- [ ] Strong `SECRET_KEY` generated
- [ ] Database connected and migrated
- [ ] Static files collected
- [ ] Health check responding at `/healthz`
- [ ] Superuser created
- [ ] Admin panel accessible
- [ ] SSL certificate active (automatic)
- [ ] Email sending works
- [ ] File uploads work
- [ ] Test user registration/login
- [ ] Test creating NFC cards
- [ ] Test public profile views
- [ ] QR codes generating correctly
- [ ] Mobile view working

---

## 🎉 Launch!

Once all checks pass:
1. Share your Render URL
2. Test from different devices
3. Monitor logs for first 24 hours
4. Set up custom domain (optional)

**Your app will be live at:**
```
https://thelastcard-web.onrender.com
```

(Replace with your actual Render URL)

---

## 🆘 Need Help?

- **Render Support**: https://render.com/support
- **Django Forum**: https://forum.djangoproject.com/
- **Check Logs**: Render Dashboard → Your Service → Logs

Good luck with your deployment! 🚀
