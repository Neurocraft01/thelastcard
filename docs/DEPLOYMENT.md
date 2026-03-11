# Production Deployment Checklist

## Pre-Deployment Security Audit

### 1. Environment Configuration ✓
- [x] Create .gitignore file (prevents sensitive files from being committed)
- [x] Remove actual credentials from .env.example
- [ ] Generate new SECRET_KEY for production (minimum 50 characters)
  ```python
  python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
  ```
- [ ] Set DEBUG=False in production .env
- [ ] Configure ALLOWED_HOSTS with actual domain(s)
- [ ] Set CSRF_TRUSTED_ORIGINS with https:// URLs

### 2. Database Configuration
- [ ] Set up PostgreSQL/Neon database
- [ ] Update DATABASE_URL in .env
- [ ] Run migrations: `python manage.py migrate`
- [ ] Create superuser: `python manage.py createsuperuser`
- [ ] Backup strategy configured

### 3. Email Configuration
- [ ] Configure SMTP settings (Gmail/SendGrid/Mailgun)
- [ ] Test email sending: `python manage.py test_email`
- [ ] Verify DEFAULT_FROM_EMAIL is correct
- [ ] Enable email verification if required

### 4. Static & Media Files
- [ ] Run collectstatic: `python manage.py collectstatic --noinput`
- [ ] Configure Cloudflare R2 or alternative storage (optional)
- [ ] Test file uploads (profile photos, logos)
- [ ] Set appropriate file size limits

### 5. Security Settings (Auto-enabled when DEBUG=False)
- [x] SECURE_SSL_REDIRECT enabled
- [x] SECURE_HSTS_SECONDS set to 31536000 (1 year)
- [x] SESSION_COOKIE_SECURE enabled
- [x] CSRF_COOKIE_SECURE enabled
- [x] X_FRAME_OPTIONS set to DENY
- [x] WhiteNoise middleware configured

### 6. Testing Before Deployment
```bash
# Comprehensive Django checks
python manage.py check --deploy

# Test all migrations are applied
python manage.py showmigrations

# Verify static files
python manage.py collectstatic --dry-run

# Check for missing templates
python manage.py check
```

### 7. Production Server Setup

#### Option A: Railway/Render/Fly.io
```bash
# Build Command:
pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate

# Start Command:
gunicorn nfc_platform.wsgi:application --bind 0.0.0.0:$PORT --workers 2 --timeout 60
```

#### Option B: Traditional VPS (DigitalOcean, AWS EC2, etc.)
```bash
# Install system dependencies
sudo apt update
sudo apt install python3-pip python3-venv nginx certbot python3-certbot-nginx

# Clone repository
git clone <repo-url>
cd customcard

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
nano .env  # Edit with production values

# Run migrations
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser

# Set up systemd service
sudo nano /etc/systemd/system/nfc-platform.service
```

**Systemd Service File:**
```ini
[Unit]
Description=NFC Platform
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/customcard
Environment="PATH=/path/to/customcard/.venv/bin"
ExecStart=/path/to/customcard/.venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 nfc_platform.wsgi:application

[Install]
WantedBy=multi-user.target
```

**Nginx Configuration:**
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location /static/ {
        alias /path/to/customcard/staticfiles/;
    }

    location /media/ {
        alias /path/to/customcard/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 8. SSL Certificate Setup
```bash
# Install Certbot
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal test
sudo certbot renew --dry-run
```

### 9. Post-Deployment Verification
- [ ] Test user registration and login
- [ ] Test email password reset flow
- [ ] Create a test NFC card order
- [ ] Verify public profile pages work (/u/username)
- [ ] Test admin dashboard access
- [ ] Verify analytics tracking works
- [ ] Test file uploads (profile photos, order designs)
- [ ] Check all static files load correctly
- [ ] Test error pages (404, 500)
- [ ] Verify mobile responsiveness

### 10. Monitoring & Maintenance
- [ ] Set up application monitoring (Sentry, New Relic, etc.)
- [ ] Configure automated backups
  ```bash
  # Database backup cron
  0 2 * * * pg_dump $DATABASE_URL > /backups/nfc_$(date +\%Y\%m\%d).sql
  ```
- [ ] Set up uptime monitoring (Pingdom, UptimeRobot)
- [ ] Configure log rotation
- [ ] Set up automated SSL renewal
- [ ] Schedule regular security updates

### 11. Performance Optimization
- [ ] Enable Redis caching (optional)
- [ ] Configure CDN for static files (Cloudflare)
- [ ] Enable gzip compression
- [ ] Set up database connection pooling
- [ ] Optimize database queries (use select_related/prefetch_related)

### 12. Final Security Checks
```bash
# Run security audit
python manage.py check --deploy

# Check for vulnerabilities
pip install safety
safety check

# Update all dependencies
pip list --outdated
```

### 13. Documentation
- [ ] Update README.md with production URLs
- [ ] Document custom configuration
- [ ] Create admin guide for client
- [ ] Provide user training materials

## Emergency Rollback Plan

If deployment fails:
```bash
# Revert migrations
python manage.py migrate app_name migration_number

# Restore database backup
pg_restore -d db_name backup_file.sql

# Revert code
git revert <commit-hash>
git push
```

## Client Handover Checklist

- [ ] Provide admin credentials (securely)
- [ ] Share production .env file (encrypted)
- [ ] Demonstrate admin panel features
- [ ] Explain order management workflow
- [ ] Show analytics dashboard
- [ ] Provide emergency contact information
- [ ] Document backup restoration procedure

## Support Contact

For deployment issues:
- Developer: your-email@domain.com
- Emergency: +1-XXX-XXX-XXXX

---

**Status**: ✅ Production Ready
**Last Updated**: February 3, 2026
**Version**: 1.0.0
