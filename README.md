# The Last Card - NFC Platform

A comprehensive NFC business card management platform built with Django 6.0.

## Features

- **Role-Based Authentication**: Super Admin, Admin, and User roles
- **Digital NFC Profiles**: Create and manage digital business cards
- **Physical Card Orders**: Order custom PVC, Metal, and Wood NFC cards
- **Real-Time Analytics**: Track profile views, interactions, and engagement
- **Theme Customization**: 15+ pre-designed themes with dark mode support
- **QR Code Generation**: Automatic QR codes for each profile
- **vCard Export**: Download contact information directly to phone
- **Simple Admin System**: Easy 3-tier role management
- **RESTful API**: Complete API for mobile app integration

## Tech Stack

- **Backend**: Django 6.0.1, Python 3.12
- **Database**: PostgreSQL (Neon) / SQLite (development)
- **Storage**: Cloudflare R2 (S3-compatible) for media files
- **Frontend**: Tailwind CSS, Material Symbols Icons
- **Authentication**: Django Allauth with Google OAuth
- **API**: Django REST Framework

## Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd customcard

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration

```bash
# Copy example environment file
cp .env.example .env

# Edit .env file with your settings
# Required: SECRET_KEY, DATABASE_URL, EMAIL settings
```

### 3. Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 4. Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 5. Run Development Server

```bash
python manage.py runserver
```

Visit http://localhost:8000

## Project Structure

```
customcard/
├── accounts/          # User authentication and roles
├── analytics/         # Profile analytics and tracking
├── api/              # REST API endpoints
├── cards/            # NFC card management
├── landing/          # Landing pages
├── orders/           # Physical card orders
├── profiles/         # User profiles and public pages
├── themes/           # Theme management
├── nfc_platform/     # Project settings
├── static/           # Static files (CSS, JS, images)
├── templates/        # HTML templates
├── media/            # User uploads
└── requirements.txt  # Python dependencies
```

## Environment Variables

### Required

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key (50+ chars) | `your-secret-key-here` |
| `DEBUG` | Debug mode (False in production) | `False` |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts | `yourdomain.com,www.yourdomain.com` |
| `DATABASE_URL` | Database connection string | `postgres://user:pass@host/db` |

### Email (Required for password reset)

| Variable | Description | Example |
|----------|-------------|---------|
| `EMAIL_HOST` | SMTP server | `smtp.gmail.com` |
| `EMAIL_PORT` | SMTP port | `587` |
| `EMAIL_HOST_USER` | Email address | `your-email@gmail.com` |
| `EMAIL_HOST_PASSWORD` | Email password/app password | `your-app-password` |

### Optional

| Variable | Description | Default |
|----------|-------------|---------|
| `USE_R2_STORAGE` | Enable Cloudflare R2 | `False` |
| `R2_ACCOUNT_ID` | Cloudflare R2 account ID | - |
| `R2_ACCESS_KEY_ID` | R2 access key | - |
| `R2_SECRET_ACCESS_KEY` | R2 secret key | - |
| `R2_BUCKET_NAME` | R2 bucket name | `nfc-platform` |

## Deployment

### Production Checklist

- [ ] Set `DEBUG=False` in .env
- [ ] Generate new `SECRET_KEY` (50+ random characters)
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Set up PostgreSQL/Neon database
- [ ] Configure email SMTP settings
- [ ] Set up Cloudflare R2 for media files (optional)
- [ ] Configure HTTPS/SSL certificates
- [ ] Run `python manage.py collectstatic`
- [ ] Run `python manage.py migrate`
- [ ] Create superuser account
- [ ] Set up monitoring and backups

### Deploy to Railway/Render/Heroku

1. **Add build command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`

2. **Add start command**: `gunicorn nfc_platform.wsgi:application --bind 0.0.0.0:$PORT`

3. **Set environment variables** from your .env file

4. **Configure custom domain** in platform settings

### Deploy with Docker (Coming Soon)

```bash
# Build image
docker build -t nfc-platform .

# Run container
docker run -p 8000:8000 --env-file .env nfc-platform
```

## Default Test Accounts

After running migrations, create these test users:

```bash
python manage.py createsuperuser --email superadmin@test.com --username superadmin
```

Then login at `/admin` to create additional test users.

## API Documentation

API endpoints are available at `/api/` with the following structure:

- `POST /api/analytics/track/` - Track profile interaction
- `GET /api/profile/` - Get current user profile
- `POST /api/profile/update/` - Update profile
- `GET /api/cards/` - List user cards
- `GET /api/themes/` - List available themes

API authentication uses session authentication (same as web interface).

## Key URLs

- **Landing Page**: `/`
- **Login**: `/login/`
- **Register**: `/register/`
- **Dashboard**: `/dashboard/` (redirects based on role)
- **Public Profile**: `/u/{username}/`
- **Admin Panel**: `/admin/`
- **API**: `/api/`

## Security Features

- **Role-Based Access Control**: Super Admin, Admin, User roles
- **Session Security**: HttpOnly, Secure cookies in production
- **CSRF Protection**: Enabled for all POST requests
- **Password Hashing**: PBKDF2 with SHA256
- **Login Attempts Tracking**: Account lockout after failed attempts
- **Email Verification**: Optional email verification on signup
- **HTTPS Enforcement**: Automatic redirect in production

## Support

For issues and questions:
- Email: support@yourdomain.com
- Documentation: https://docs.yourdomain.com

## License

Proprietary - All Rights Reserved

## Credits

Built with ❤️ for seamless digital networking
