# 🚀 QUICK RENDER CONFIGURATION REFERENCE

## Copy-Paste Values for Render Dashboard

### ⚙️ Service Configuration

**Name:**
```
thelastcard-web
```

**Region:**
```
Oregon
```

**Branch:**
```
main
```

**Runtime:**
```
Python 3
```

**Build Command:**
```
./build.sh
```

**Start Command:**
```
gunicorn nfc_platform.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120
```

**Plan:**
```
Starter ($7/month)
```

---

### 🔍 Health Check Configuration

**Health Check Path:**
```
/healthz
```

**Health Check Interval:** `30 seconds`
**Health Check Timeout:** `10 seconds`
**Health Check Threshold:** `3 failures`

---

### 📋 Environment Variables (Add in Advanced Settings)

Copy ALL of these and paste one by one:

```
DEBUG=False
```

```
PYTHON_VERSION=3.12.2
```

```
SECRET_KEY=GENERATE-NEW-KEY-USE-COMMAND-BELOW
```

**Generate SECRET_KEY with:**
```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

```
DATABASE_URL=postgresql://neondb_owner:npg_y8FMp0XVKHLW@ep-dark-wildflower-aizjaibz-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require
```

```
ALLOWED_HOSTS=thelastcard-web.onrender.com,localhost,127.0.0.1
```

```
CSRF_TRUSTED_ORIGINS=https://thelastcard-web.onrender.com,http://localhost:8000
```

```
SITE_URL=https://thelastcard-web.onrender.com
```

```
SITE_NAME=The Last Card
```

```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
```

```
EMAIL_HOST=smtp.gmail.com
```

```
EMAIL_PORT=587
```

```
EMAIL_USE_TLS=True
```

```
EMAIL_HOST_USER=thelastcardnfc@gmail.com
```

```
EMAIL_HOST_PASSWORD=zcys rdfo aieo bmla
```

```
DEFAULT_FROM_EMAIL=The Last Card <thelastcardnfc@gmail.com>
```

---

### 🔨 Build Filters (Optional)

**Ignored Paths** (prevents deploy on documentation changes):

```
*.md
```

```
design/**
```

```
scripts/**
```

```
.vscode/**
```

```
media/**
```

---

### ⚡ Auto-Deploy Settings

**Auto-Deploy:** ✅ Enabled
**Trigger:** On commit to `main` branch

---

### 📝 Pre-Deploy Command (Alternative to build.sh)

If build.sh doesn't work, use this in "Pre-Deploy Command" field:

```
pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate --no-input
```

---

### 🗄️ PostgreSQL Database (If using Render DB instead of Neon)

**Name:**
```
thelastcard-db
```

**Database Name:**
```
thelastcard
```

**User:**
```
thelastcard_user
```

**Region:**
```
Oregon
```

**Plan:**
```
Starter (Free)
```

Then copy the **Internal Database URL** and use it in `DATABASE_URL` environment variable.

---

### ✅ Quick Verification After Deploy

1. **Health Check:**
   ```
   https://thelastcard-web.onrender.com/healthz
   ```
   Should return: `{"status":"healthy","database":"connected"}`

2. **Admin Panel:**
   ```
   https://thelastcard-web.onrender.com/admin/
   ```

3. **Landing Page:**
   ```
   https://thelastcard-web.onrender.com/
   ```

---

### 🔧 Troubleshooting Commands

**View Logs in Render Shell:**
```bash
# Check recent logs
tail -f /var/log/render.log

# Check migrations
python manage.py showmigrations

# Create superuser
python manage.py createsuperuser

# Test database
python manage.py dbshell
```

---

### 📊 Performance Settings for $7 Plan

Your current Gunicorn config is optimized for 512MB RAM:
- **Workers:** 2
- **Threads:** 4 per worker
- **Timeout:** 120 seconds
- **Total concurrent requests:** 8

If you experience memory issues, reduce to:
```
gunicorn nfc_platform.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 120
```

---

### 🌐 Custom Domain Setup (After Deployment)

1. **Add Custom Domain in Render:**
   - Go to Settings → Custom Domains
   - Add your domain (e.g., `thelastcard.in`)

2. **Update DNS Records:**
   ```
   Type: CNAME
   Name: www (or @)
   Value: thelastcard-web.onrender.com
   ```

3. **Update Environment Variables:**
   ```
   ALLOWED_HOSTS=thelastcard.in,www.thelastcard.in,thelastcard-web.onrender.com
   CSRF_TRUSTED_ORIGINS=https://thelastcard.in,https://www.thelastcard.in,https://thelastcard-web.onrender.com
   SITE_URL=https://thelastcard.in
   ```

---

### 🎯 Important Notes

⚠️ **After Deploy, Update These Variables:**

Once Render assigns your actual URL (e.g., `thelastcard-web-xyz.onrender.com`), update:
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `SITE_URL`

⚠️ **First Deploy Takes Longer:**
- Initial deploy: 5-10 minutes
- Subsequent deploys: 2-5 minutes
- Includes: Install dependencies, collect static files, run migrations

⚠️ **Free Plan Limitations:**
- Service spins down after 15 min of inactivity
- First request after spin-down: slower (30-60 seconds)
- $7 Starter plan: No spin-down!

---

### ✨ Post-Deploy Tasks

1. ✅ Create superuser
2. ✅ Test admin login
3. ✅ Create test NFC card
4. ✅ Test public profile view
5. ✅ Test QR code generation
6. ✅ Test email sending (registration)
7. ✅ Test file uploads
8. ✅ Monitor logs for first hour

---

**Need the full guide?** See `RENDER_DEPLOYMENT.md`

**Ready to deploy?** Push your code and create the web service! 🚀
